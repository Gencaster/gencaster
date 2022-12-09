<template>
  <div class="index-page">
    <h1>Gencaster Stream</h1>
    <p>
      <span>Currently on stream: {{ streamId }}</span>
    </p>
    <audio ref="player" controls />
    <p>
      <button @click="startMicStreaming()">
        Start microphone
      </button>
    </p>
    <p>
      <button @click="stopMicStreaming()">
        Stop microphone
      </button>
    </p>
  </div>
</template>

<script>
export default {
  name: "IndexComponent",
  components: {},
  data() {
    return {
      params: {
        opaqueIdAppendix: "streamingtest-",
        iceServers: "stun:stun.l.google.com:19302"
      },
      logs: [],
      formData: {
        emit: "",
        broadcast: "",
        joinRoom: "",
        leaveRoom: "",
        sendRoomName: "",
        sendRoomMessage: "",
        closeRoom: ""
      },
      streamId: "",
      // internal
      Janus: null,
      janusInstance: null,
      streaming: null,
      mixertest: null
    };
  },
  head() {
    return {
      script: [
        {
          src: "https://cdnjs.cloudflare.com/ajax/libs/webrtc-adapter/8.1.0/adapter.min.js",
          body: true
        },
        {
          src: "https://cdn.jsdelivr.net/npm/janus-gateway@0.2.3/html/janus.nojquery.js",
          body: true
        }
      ]
    };
  },
  computed: {},
  mounted() {
    this.initJanus();
  },
  created() {},
  methods: {
    initJanus() {
      this.Janus = Janus;

      // eslint-disable-next-line @typescript-eslint/no-this-alias
      const that = this;
      let audioBridgeWebRtcUp = false;
      const { hostname, protocol } = window.location;

      const server
        = protocol === "http:"
          ? `http://${hostname}:8088/janus`
          : `https://${hostname}:8089/janus`;

      const opaqueId
        = this.params.opaqueIdAppendix + this.Janus.randomString(12);
      const sendOpaqueId = `streaming-${this.Janus.randomString(12)}`;

      this.audioElem = this.$refs.player;
      this.Janus.init({
        debug: "all",
        callback: () => {
          // Make sure the browser supports WebRTC
          // [] To do: Send to page explaining webrtc support needed
          if (!this.Janus.isWebrtcSupported()) {
            alert(
              "Unfortunately, your devices doesn't seem to support WebRTC."
            );
            return;
          }
          // Create session
          that.janusInstance = new this.Janus({
            server,
            // TODO: needed?
            iceServers: [{ urls: this.params.iceServers }],
            success: () => {
              // attach to audiobridge
              that.janusInstance.attach({
                plugin: "janus.plugin.audiobridge",
                opaqueId: sendOpaqueId,
                success(pluginHandle) {
                  that.mixertest = pluginHandle;
                  Janus.log("Audiobridge attached");
                },
                onmessage(msg, jsep) {
                  Janus.debug(" ::: Got a message :::", msg);
                  const event = msg.audiobridge;
                  Janus.debug(`Event: ${event}`);
                  if (event) {
                    if (event === "joined") {
                      // Successfully joined, negotiate WebRTC now
                      if (msg.id) {
                        Janus.log(`Successfully joined room ${msg.room}`);
                        if (!audioBridgeWebRtcUp) {
                          audioBridgeWebRtcUp = true;
                          // Publish our stream
                          that.mixertest.createOffer({
                            media: { video: false }, // This is an audio only room
                            customizeSdp(jsep) {
                              if (!jsep.sdp.includes("stereo=1")) {
                                // Make sure that our offer contains stereo too
                                jsep.sdp = jsep.sdp.replace(
                                  "useinbandfec=1",
                                  "useinbandfec=1;stereo=1"
                                );
                              }
                            },
                            success(jsep) {
                              Janus.debug("Got SDP!", jsep);
                              const publish = {
                                request: "configure",
                                muted: false
                              };
                              that.mixertest.send({ message: publish, jsep });
                            },
                            error(error) {
                              Janus.error(`WebRTC error: ${error}`);
                            }
                          });
                        }
                      }
                    }
                    else if (event === "event") {
                      if (msg.error) {
                        console.log(msg.error);
                        return;
                      }
                    }
                  }
                  if (jsep) {
                    Janus.debug("Handling SDP as well...", jsep);
                    that.mixertest.handleRemoteJsep({ jsep });
                  }
                }
              });
              // Attach to Streaming plugin
              that.janusInstance.attach({
                plugin: "janus.plugin.streaming",
                opaqueId,
                success: (pluginHandle) => {
                  that.streaming = pluginHandle;
                  console.log(
                    `Plugin attached! (${that.streaming.getPlugin()}, id=${that.streaming.getId()})`
                  );
                  // Setup streaming session
                  that.updateStreamsList();
                },
                error(error) {
                  console.error("  -- Error attaching plugin... ", error);
                  alert(`Error attaching plugin... ${error}`);
                },
                iceState(state) {
                  console.log(`ICE state changed to ${state}`);
                },
                webrtcState(on) {
                  console.log(
                    `Janus says our WebRTC PeerConnection is ${
                      on ? "up" : "down"
                    } now`
                  );
                },
                onmessage(msg, jsep) {
                  console.log(" ::: Got a message :::", msg);
                  if (jsep) {
                    console.log("Handling SDP as well...", jsep);
                    // eslint-disable-next-line unicorn/prefer-includes
                    const stereo = jsep.sdp.indexOf("stereo=1") !== -1;
                    // Offer from the plugin, let's answer
                    that.streaming.createAnswer({
                      jsep,
                      // We want recvonly audio/video and, if negotiated, datachannels
                      media: { audioSend: false, videoSend: false, data: true },
                      customizeSdp(jsep) {
                        // eslint-disable-next-line unicorn/prefer-includes
                        if (stereo && jsep.sdp.indexOf("stereo=1") === -1) {
                          // Make sure that our offer contains stereo too
                          jsep.sdp = jsep.sdp.replace(
                            "useinbandfec=1",
                            "useinbandfec=1;stereo=1"
                          );
                        }
                      },
                      success(jsep) {
                        console.log("Got SDP!", jsep);
                        const body = { request: "start" };
                        that.streaming.send({ message: body, jsep });
                      },
                      error(error) {
                        console.error("WebRTC error:", error);
                        alert(`WebRTC error... ${error.message}`);
                      }
                    });
                  }
                },
                onremotestream(stream) {
                  console.log(" ::: Got a remote stream :::", stream);
                  that.Janus.attachMediaStream(that.audioElem, stream);
                  that.audioElem.volume = 1;
                },
                oncleanup() {
                  console.log(" ::: Got a cleanup notification :::");
                }
              });
            },
            error(error) {
              console.error(error);
            },
            destroyed() {
              console.log("destroyed");
            }
          });
        }
      });
    },

    startMicStreaming() {
      console.log("Start mic streaming");
      this.mixertest.send({
        message: {
          request: "join",
          room: this.streamId
        }
      });
    },

    stopMicStreaming() {
      console.log("Stop mic streaming");
      this.mixertest.send({
        message: {
          request: "leave"
        }
      });
    },

    updateStreamsList() {
      // eslint-disable-next-line @typescript-eslint/no-this-alias
      const that = this;
      const body = { request: "list" };
      console.log("Sending message:", body);

      this.streaming.send({
        message: body,
        success(result) {
          if (!result) {
            alert("Got no response to our query for available streams");
            return;
          }

          if (result.list) {
            const list = result.list;
            console.log("Got a list of available streams");
            console.log(list);
            for (const mp in list) {
              console.log(
                `>> [${list[mp].id}] ${list[mp].description} (${list[mp].type})`
              );
            }

            // start random one
            if (list && list[0]) {
              const randomStream
                = list[Math.floor(Math.random() * list.length)];
              // alert(`Use stream ${randomStream.id}`);
              that.streamId = randomStream.id;
              const body = {
                request: "watch",
                id: randomStream.id
              };
              console.log(body);
              that.streaming.send({ message: body });
            }
          }
        }
      });
    }
  }
};
</script>

<style scoped lang="scss"></style>
