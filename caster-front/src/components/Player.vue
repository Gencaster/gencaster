<script lang="ts" setup>
import { storeToRefs } from "pinia";
import type { Ref } from "vue";
import { onMounted, onUpdated, ref } from "vue";

let audioBridgeWebRtcUp = false;
const { hostname, protocol } = window.location;
const server
  = protocol === "http:"
    ? `http://${hostname}:8088/janus`
    : `https://${hostname}:8089/janus`;

// @ts-expect-error: janus is an old library w/o es support
const Janus = window.Janus;
let mixertest: any = null;
let streaming: any = null;

const audioPlayer: any = ref(null);

let janusInstance: any;

const changeStream = () => {
  console.log("Change stream");
};

const opaqueId = `GenCaster_${Janus.randomString(12)}`;
const sendOpaqueId = `GenCasterSend_${Janus.randomString(12)}`;

const makeJanusMicOffer = () => {
  mixertest.createOffer({
    media: { video: false }, // This is an audio only room
    customizeSdp(jsep: any) {
      if (!jsep.sdp.includes("stereo=1")) {
        // Make sure that our offer contains stereo too
        jsep.sdp = jsep.sdp.replace(
          "useinbandfec=1",
          "useinbandfec=1;stereo=1"
        );
      }
    },
    success(jsep: any) {
      Janus.debug("Got SDP!", jsep);
      const publish = {
        request: "configure",
        muted: false
      };
      mixertest.send({ message: publish, jsep });
    },
    error(error: any) {
      Janus.error(`WebRTC error: ${error}`);
    }
  });
};

const setupJanusAudioBridge = () => {
  janusInstance.attach({
    plugin: "janus.plugin.audiobridge",
    opaqueId: sendOpaqueId,
    success(pluginHandle: any) {
      mixertest = pluginHandle;
      Janus.log("Audiobridge attached");
    },
    onmessage(msg: any, jsep: any) {
      const event = msg.audiobridge;
      switch (event) {
        case "joined":
          Janus.log(`Successfully joined room ${msg.room}`);
          if (audioBridgeWebRtcUp)
            return;
          audioBridgeWebRtcUp = true;
          makeJanusMicOffer();
          break;
        case "event":
          console.log("Error on sending stream", msg.error);
          break;
      }
      if (jsep)
        mixertest.handleRemoteJsep({ jsep });
    }
  });
};

const updateStreamsList = () => {
  // eslint-disable-next-line @typescript-eslint/no-this-alias
  const that = this;
  const body = { request: "list" };
  console.log("Sending message:", body);
  streaming.send({
    message: body,
    success(result: any) {
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
          const randomStream = list[Math.floor(Math.random() * list.length)];
          // alert(`Use stream ${randomStream.id}`);
          const streamId = randomStream.id;
          const body = {
            request: "watch",
            id: randomStream.id
          };
          console.log(body);
          streaming.send({ message: body });
        }
      }
    }
  });
};

const setupJanusStreaming = () => {
  console.log("Setup streaming");
  janusInstance.attach({
    plugin: "janus.plugin.streaming",
    opaqueId,
    success: (pluginHandle: any) => {
      streaming = pluginHandle;
      console.log(`Plugin attached! (${streaming.getPlugin()}, id=${streaming.getId()})`);
      // Setup streaming session
      updateStreamsList();
    },
    error(error: any) {
      console.error("  -- Error attaching plugin... ", error);
      alert(`Error attaching plugin... ${error}`);
    },
    iceState(state: any) {
      console.log(`ICE state changed to ${state}`);
    },
    webrtcState(on: any) {
      console.log(`Janus says our WebRTC PeerConnection is ${on ? "up" : "down"} now`);
    },
    onmessage(msg: any, jsep: any) {
      console.log(" ::: Got a message :::", msg);
      if (jsep) {
        console.log("Handling SDP as well...", jsep);
        // eslint-disable-next-line unicorn/prefer-includes
        const stereo = jsep.sdp.indexOf("stereo=1") !== -1;
        // Offer from the plugin, let's answer
        streaming.createAnswer({
          jsep,
          // We want recvonly audio/video and, if negotiated, datachannels
          media: { audioSend: false, videoSend: false, data: true },
          customizeSdp(jsep: any) {
            // eslint-disable-next-line unicorn/prefer-includes
            if (stereo && jsep.sdp.indexOf("stereo=1") === -1) {
              // Make sure that our offer contains stereo too
              jsep.sdp = jsep.sdp.replace(
                "useinbandfec=1",
                "useinbandfec=1;stereo=1"
              );
            }
          },
          success(jsep: any) {
            console.log("Got SDP!", jsep);
            const body = { request: "start" };
            streaming.send({ message: body, jsep });
          },
          error(error: any) {
            console.error("WebRTC error:", error);
            alert(`WebRTC error... ${error.message}`);
          }
        });
      }
    },
    onremotestream(stream: any) {
      console.log(" ::: Got a remote stream :::", stream);
      Janus.attachMediaStream(audioPlayer.value, stream);
      audioPlayer.value.volume = 1;
    },
    oncleanup() {
      console.log(" ::: Got a cleanup notification :::");
    }
  });
};

const initJanus = () => {
  console.log("Start janus");
  Janus.init({
    debug: "none",
    callback: () => {
      if (!Janus.isWebrtcSupported()) {
        alert("Unfortunately, your devices doesn't seem to support WebRTC.");
        return;
      }
      console.log("Something happened");
      janusInstance = new Janus({
        server,
        iceServers: [{ urls: "stun:stun.l.google.com:19302" }],
        success: () => {
          setupJanusAudioBridge();
          setupJanusStreaming();
        },
        error: (error: any) => {
          console.log(error);
        }
      });
    }
  });
};

const startMicStreaming = () => {
  console.log("Start mic streaming");
  mixertest.send({
    message: {
      request: "join",
      room: 1
    }
  });
};

const stopMicStreaming = () => {
  console.log("Stop mic streaming");
  mixertest.send({
    message: {
      request: "leave"
    }
  });
};

initJanus();
</script>

<template>
  <h3>Player</h3>

  <audio ref="audioPlayer" controls />
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
</template>
