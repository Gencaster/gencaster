<script setup lang="ts">
import { ElButton, ElCol, ElRow } from "element-plus";
import { storeToRefs } from "pinia";
import { usePlayerStore } from "@/stores/Player";

const { play, micActive, streamGPS } = storeToRefs(usePlayerStore());
</script>

<template>
  <div class="player-buttions">
    <ElRow :gutter="10">
      <ElCol :xs="24" :span="8">
        <ElButton
          size="large"
          type="default"
          style="width: 100%;"
          @click="play = !play"
        >
          {{ play ? "Stop" : "Play" }} Stream
        </ElButton>
      </ElCol>
      <ElCol :xs="24" :span="8">
        <ElButton
          size="large"
          type="default"
          style="width: 100%;"
          @click="micActive = !micActive"
        >
          {{ !micActive ? "Activate" : "Disable" }} Microphone
        </ElButton>
      </ElCol>
      <ElCol :xs="24" :span="8">
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
