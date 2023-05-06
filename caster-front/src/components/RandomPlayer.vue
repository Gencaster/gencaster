<script setup lang="ts">
import { ElButton, ElCollapse, ElCollapseItem } from "element-plus";
import { type Ref, computed, ref } from "vue";
import { storeToRefs } from "pinia";
import StreamInfo from "./StreamInfo.vue";
import StreamPoints from "@/components/StreamPoints.vue";
import { type StreamPoint, useStreamPointsQuery } from "@/graphql";
import PlayerButtons from "@/components/PlayerButtons.vue";
import Player from "@/components/Player.vue";
import { usePlayerStore } from "@/stores/Player";

const { data } = useStreamPointsQuery();

const selectedStreamPoint = computed<StreamPoint | undefined>(() => {
  if (data.value)
    return data.value.streamPoints[Math.floor(Math.random() * data.value.streamPoints.length)];
  return undefined;
});
</script>

<template>
  <div class="debug-player">
    <h4>Random player</h4>

    <div v-if="selectedStreamPoint">
      Stream {{ selectedStreamPoint.port }}
      <PlayerButtons
        play-button
      />
      <Player
        :stream-point="selectedStreamPoint"
      />
    </div>
    <div v-else>
      Waiting for stream
    </div>
  </div>
</template>
