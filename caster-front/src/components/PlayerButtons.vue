<script setup lang="ts">
import { ElButton, ElCol, ElRow } from "element-plus";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";
import { computed } from "vue";
import { usePlayerStore } from "@/stores/Player";

const props = withDefaults(defineProps<{
  playButton?: boolean
  micButton?: boolean
  gpsButton?: boolean
}>(), {
  playButton: true,
  micButton: false,
  gpsButton: false
});

const { play, micActive, streamGPS } = storeToRefs(usePlayerStore());

const router = useRouter();

const showPlayButton = computed<boolean>(() => router.currentRoute.value.query.play === null || props.playButton);
const showMicButton = computed<boolean>(() => router.currentRoute.value.query.mic === null || props.micButton);
const showGpsButton = computed<boolean>(() => router.currentRoute.value.query.gps === null || props.gpsButton);

const spanWidth = computed<number>(() =>
  24 / (Number(showPlayButton.value) + Number(showMicButton.value) + Number(showGpsButton.value))
);
</script>

<template>
  <div class="player-buttons">
    <ElRow :gutter="10">
      <ElCol v-if="showPlayButton" :xs="24" :span="spanWidth">
        <ElButton
          size="large"
          type="default"
          style="width: 100%;"
          @click="play = !play"
        >
          {{ play ? "Stop" : "Play" }} Stream
        </ElButton>
      </ElCol>
      <ElCol v-if="showMicButton" :xs="24" :span="spanWidth">
        <ElButton
          size="large"
          type="default"
          style="width: 100%;"
          @click="micActive = !micActive"
        >
          {{ !micActive ? "Activate" : "Disable" }} Microphone
        </ElButton>
      </ElCol>
      <ElCol v-if="showGpsButton" :xs="24" :span="spanWidth">
        <ElButton
          size="large"
          type="default"
          style="width: 100%;"
          @click="streamGPS = !streamGPS"
        >
          {{ !streamGPS ? "Activate" : "Disable" }} GPS
        </ElButton>
      </ElCol>
    </ElRow>
  </div>
</template>
