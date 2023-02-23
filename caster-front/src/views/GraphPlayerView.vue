<script setup lang="ts">
import { storeToRefs } from "pinia";
import { onMounted, watch } from "vue";
import Player from "@/components/Player.vue";
import PlayerControls from "@/components/PlayerControls.vue";

import { useGraphsStore } from "@/stores/Graphs";
import { usePlayerStore } from "@/stores/Player";
import router from "@/router/index";
import StreamPointInfo from "@/components/StreamPointInfo.vue";

const { selectedGraph } = storeToRefs(useGraphsStore());
const { graphUuid, streamInfo, activeStreamPoint } = storeToRefs(usePlayerStore());

onMounted(() => {
  graphUuid.value = router.currentRoute.value.params.graphUuid;
});

watch(streamInfo, (info) => {
  if (info?.streamInfo.__typename === "StreamInfo")
    activeStreamPoint.value = info.streamInfo.stream.streamPoint;
});

// @todo get graph name?
</script>

<template>
  <main>
    <h1>Graph {{ selectedGraph?.name }}</h1>
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>Player</span>
          <PlayerControls />
        </div>
      </template>
      <Player />
      <div v-if="streamInfo?.streamInfo.__typename === `StreamInfo`">
        <StreamPointInfo />
        <h3>Instruction</h3>
        {{ streamInfo?.streamInfo.streamInstruction?.instructionText }}
      </div>
      <div v-else>
        Failed to get stream: {{ streamInfo?.streamInfo.error }}
      </div>
    </el-card>
  </main>
</template>
