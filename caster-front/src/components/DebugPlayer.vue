<script setup lang="ts">
import { ElButton, ElCollapse, ElCollapseItem } from "element-plus";
import { type Ref, computed, ref } from "vue";
import { storeToRefs } from "pinia";
import StreamInfo from "./StreamInfo.vue";
import StreamPoints from "@/components/StreamPoints.vue";
import type { StreamPoint } from "@/graphql";
import PlayerButtons from "@/components/PlayerButtons.vue";
import Player from "@/components/Player.vue";
import { usePlayerStore } from "@/stores/Player";

const selectedStreamPoint: Ref<StreamPoint | undefined> = ref();

const { micActive, streamGPS, play } = storeToRefs(usePlayerStore());

const streamInfo = computed(() => {
  return {
    uuid: "",
    streamPoint: selectedStreamPoint.value
  };
});

const resetStreamPoint = () => {
  micActive.value = false;
  streamGPS.value = false;
  play.value = false;
  selectedStreamPoint.value = undefined;
};
</script>

<template>
  <div class="debug-player">
    <h4>Debug Player</h4>

    <ElCollapse>
      <ElCollapseItem title="Streaming points">
        <StreamPoints
          @selected-stream-point="(streamPoint) => selectedStreamPoint = streamPoint"
        />
        <ElButton
          style="width: 100%; margin-top: 10px;"
          @click="resetStreamPoint()"
        >
          Reset streaming point
        </ElButton>
      </ElCollapseItem>
      <ElCollapseItem title="Player">
        <div v-if="selectedStreamPoint">
          <PlayerButtons
            play-button
            mic-button
            gps-button
          />
          <Player
            :stream-point="selectedStreamPoint"
          />
        </div>
        <div v-else>
          Please select a streaming point first
        </div>
      </ElCollapseItem>
      <ElCollapseItem title="Debug info">
        <div v-if="selectedStreamPoint">
          <StreamInfo
            :stream="streamInfo"
          />
        </div>
        <div v-else>
          <span>No stream selected</span>
        </div>
      </ElCollapseItem>
    </ElCollapse>
  </div>
</template>
