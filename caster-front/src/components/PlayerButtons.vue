<script setup lang="ts">
import { ElButton, ElCol, ElRow } from "element-plus";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";
import { usePlayerStore } from "@/stores/Player";

const { play, micActive, streamGPS } = storeToRefs(usePlayerStore());

const router = useRouter();
</script>

<template>
  <div class="player-buttons">
    <ElRow :gutter="10">
      <ElCol :xs="24" :span="24">
        <ElButton
          size="large"
          type="default"
          style="width: 100%;"
          @click="play = !play"
        >
          {{ play ? "Stop" : "Play" }} Stream
        </ElButton>
      </ElCol>
      <ElCol v-if="router.currentRoute.value.query.mic === null" :xs="24" :span="24">
        <ElButton
          size="large"
          type="default"
          style="width: 100%;"
          @click="micActive = !micActive"
        >
          {{ !micActive ? "Activate" : "Disable" }} Microphone
        </ElButton>
      </ElCol>
      <ElCol v-if="router.currentRoute.value.query.gps === null" :xs="24" :span="24">
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
