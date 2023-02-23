<script lang="ts" setup>
import { storeToRefs } from "pinia";
import type { Ref } from "vue";
import { ref, watch } from "vue";
import { usePlayerStore } from "@/stores/Player";

defineProps({
  showPlayer: {
    type: Boolean,
    default: false
  },
  showRawControls: {
    type: Boolean,
    default: false
  },
  showPlayerInfo: {
    type: Boolean,
    default: false
  },
  showStreamInfo: {
    type: Boolean,
    default: false
  }
});

const { micActive, play, streamInfo, activeStreamPoint } = storeToRefs(usePlayerStore());

let audioBridgeWebRtcUp = false;
const { hostname, protocol } = window.location;
const windowServer
  = protocol === "http:"
    ? `http://${hostname}:8088/janus`
    : `https://${hostname}:8089/janus`;

const envServer = import.meta.env.VITE_JANUS_URL;
const server = envServer === undefined ? windowServer : envServer;

// @ts-expect-error: janus is an old library w/o es support
const Janus = window.Janus;
let audioBridge: any = null;
let streaming: any = null;
const streamingConnected: Ref<boolean> = ref(false);
const audioBridgeConnected: Ref<boolean> = ref(false);

const audioPlayer: any = ref(null);

let janusInstance: any;

const opaqueId = `GenCaster_${Janus.randomString(12)}`;
const sendOpaqueId = `GenCasterSend_${Janus.randomString(12)}`;

const switchAudioBridgeRoom = (roomId: number) => {
  audioBridge.send({
    message: {
      request: audioBridgeConnected.value ? "changeroom" : "join",
      room: roomId
    }
  });
  audioBridgeConnected.value = true;
};

const makeJanusMicOffer = () => {
  audioBridge.createOffer({
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
      const publish = {
        request: "configure",
        muted: false
      };
      audioBridge.send({ message: publish, jsep });
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
      audioBridge = pluginHandle;
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
        audioBridge.handleRemoteJsep({ jsep });
    }
  });
};

const switchStream = (streamId: number) => {
  streaming.send({
    message: {
      // on first connection we need to use the watch endpoint
      request: streamingConnected.value ? "switch" : "watch",
      id: streamId
    }
  });
  streamingConnected.value = true;
};

const getJanusStreamPoints = () => {
  /* Legacy function which queries janus directly
  for all streaming channels.
  This may be interesting when using Gencaster without backend
  as in its current state the backend is responsible to assign
  a stream point to a user.
  */
  streaming.send({
    message: { request: "list" },
    success(result: any) {
      if (!result) {
        console.log("Got no response to our query for available streams");
        return;
      }
      if (result.list)
        console.log("Got a list of available streams", result.list);
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
    },
    error(error: any) {
      console.error("  -- Error attaching plugin... ", error);
    },
    iceState(state: any) {
      console.log(`ICE state changed to ${state}`);
    },
    webrtcState(on: any) {
      console.log(`Janus says our WebRTC PeerConnection is ${on ? "up" : "down"} now`);
    },
    onmessage(msg: any, jsep: RTCSessionDescription) {
      if (jsep) {
        // eslint-disable-next-line unicorn/prefer-includes
        const stereo = jsep.sdp.indexOf("stereo=1") !== -1;
        // Offer from the plugin, let's answer
        streaming.createAnswer({
          jsep,
          // We want recvonly audio/video and, if negotiated, datachannels
          media: { audioSend: false, videoSend: false, data: true },
          customizeSdp(jsep: RTCSessionDescription) {
            // eslint-disable-next-line unicorn/prefer-includes
            if (stereo && jsep.sdp.indexOf("stereo=1") === -1) {
              // Make sure that our offer contains stereo too
              // @ts-expect-error: sdp seems readonly but we ignore it
              jsep.sdp = jsep.sdp.replace(
                "useinbandfec=1",
                "useinbandfec=1;stereo=1"
              );
            }
          },
          success(jsep: RTCSessionDescription) {
            const body = { request: "start" };
            streaming.send({ message: body, jsep });
          },
          error(error: any) {
            console.error("WebRTC error:", error);
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

const stopMicStreaming = () => {
  console.log("Stop mic streaming");
  audioBridge.send({
    message: {
      request: "leave"
    }
  });
};

watch(activeStreamPoint, (newStreamPoint) => {
  if (newStreamPoint === undefined)
    return;

  console.log("Change to stream", newStreamPoint);
  if (newStreamPoint.janusOutRoom)
    switchStream(newStreamPoint.janusOutRoom);
  if (newStreamPoint.janusInRoom && micActive.value)
    switchAudioBridgeRoom(newStreamPoint.janusInRoom);
});

watch(micActive, (micState) => {
  console.log(`Change mic status to ${micState}`);
  if (micState === false) {
    stopMicStreaming();
    return;
  }
  if (activeStreamPoint.value === undefined)
    return;
  if (activeStreamPoint.value.janusInRoom)
    switchAudioBridgeRoom(activeStreamPoint.value.janusInRoom);
});

watch(play, (playState) => {
  console.log(`Change play status to ${playState}`);
  playState ? audioPlayer.value.play() : audioPlayer.value.pause();
});

initJanus();
</script>

<template>
  <audio ref="audioPlayer" controls :hidden="showPlayer ? false : true " />

  <div v-if="showRawControls" class="player-control">
    <button :disabled="activeStreamPoint === null" @click="() => { play = true }">
      Play
    </button>
    <button :disabled="activeStreamPoint === null" @click="() => { play = false }">
      Pause
    </button>
    <button @click="() => { micActive = !micActive }">
      Change mic status
    </button>
  </div>

  <div v-if="showPlayerInfo" class="player-info">
    <span>Currently on stream {{ activeStreamPoint?.port }} (Janus ID {{ activeStreamPoint?.janusOutRoom }})</span><br>
    <span>Mic is active: {{ micActive }}</span>
  </div>

  <div v-if="showStreamInfo" class="stream-info">
    <div v-if="streamInfo?.streamInfo.__typename === `NoStreamAvailableError`">
      Currently no stream is available
    </div>
    <div v-else>
      <span>Assigned stream {{ streamInfo?.streamInfo.stream.streamPoint.port }}</span><br>
      <span>Current instruction</span><br>
      <span style="font-family: monospace;">{{ streamInfo?.streamInfo.streamInstruction?.instructionText }}</span>
    </div>
  </div>
</template>
