<script setup lang="ts">
import { storeToRefs } from "pinia";
import { watch } from "vue";
import StreamPoints from "../components/StreamPoints.vue";
import Player from "../components/Player.vue";
import Graphs from "../components/Graphs.vue";
import { useStreamPointsStore } from "@/stores/StreamPoints";
import { usePlayerStore } from "@/stores/Player";

const { selectedStreamPoint } = storeToRefs(useStreamPointsStore());
const { activeStreamPoint } = storeToRefs(usePlayerStore());

watch(selectedStreamPoint, (newStreamPoint) => {
  activeStreamPoint.value = newStreamPoint;
});
</script>

<template>
  <main>
    <h2>Graphs</h2>
    <Graphs />
    <h2>Stream Points</h2>
    <StreamPoints />
    <h2>Player</h2>
    <Player
      show-player
      show-player-info
      show-raw-controls
      show-stream-info
    />
  </main>
</template>
