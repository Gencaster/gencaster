<script setup lang="ts">
import PlayerVisualizer from "@/components/PlayerVisualizer/PlayerVisualizer.vue";
import { computed } from "vue";
import { type StreamPoint, useStreamPointsQuery } from "@/graphql";
import PlayerButtons from "@/components/PlayerButtons.vue";
import Player from "@/components/PlayerComponent.vue";

const { data } = useStreamPointsQuery();
const selectedStreamPoint = computed<StreamPoint | undefined>(() => {
  if (data.value)
    return data.value.streamPoints[
      Math.floor(Math.random() * data.value.streamPoints.length)
    ];
  return undefined;
});
</script>

<template>
  <div class="debug-player">
    <h3 class="invert">
      Gencaster Livecoding
    </h3>

    <div v-if="selectedStreamPoint">
      Stream {{ selectedStreamPoint.port }}
      <center style="margin-top: 100px">
        <PlayerButtons play-button />
      </center>
      <Player :stream-point="selectedStreamPoint" />
      <PlayerVisualizer />
    </div>
    <div v-else>
      Waiting for stream
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/variables.scss";
.invert {
  background-color: $green-light;
}

.audio-visualizer {
  box-sizing: border-box;
  position: absolute;
  top: 20px;
  left: 0px;
  height: 80px;
  width: 100%;
  padding-left: 24px;
  padding-right: 24px;
  margin: 0 auto;
}
</style>
