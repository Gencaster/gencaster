<script setup lang="ts">
import { type Ref, computed, ref } from "vue";
import { ElCollapse, ElCollapseItem } from "element-plus";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";

import Player from "@/components/Player.vue";
import PlayerVisualizer from "@/components/PlayerVisualizer/PlayerVisualizer.vue";
import PlayerBar from "@/components/PlayerBar/PlayerBar.vue";
import StreamInfo from "@/components/StreamInfo.vue";
import EndScreen from "@/components/EndScreen.vue";
import Content from "@/components/Content.vue";
import DataPopups from "@/components/DataPopups.vue";
import AudioInfo from "@/components/AudioInfo.vue";
import Intro from "@/components/Intro.vue";

import { PlayerState } from "@/models";
import type { Graph } from "@/graphql";
import { useStreamSubscription } from "@/graphql";
import { usePlayerStore } from "@/stores/Player";
const props = defineProps<{
  graph: Pick<Graph, "uuid" | "name">
}>();

const {
  playerState,
  infoContent,
  showInfo
} = storeToRefs(usePlayerStore());

const router = useRouter();
// const showDebug = computed<boolean>(() => router.currentRoute.value.query.debug === null);
const showDebug = true;

const { data, error, stale } = useStreamSubscription({
  variables: {
    graphUuid: props.graph.uuid
  },
  pause: router.currentRoute.value.name !== "graphPlayer"
});

const accorrdionNamespaceOpen = "debug";
const playerRef: Ref<InstanceType<typeof Player> | undefined> = ref(undefined);

const hasInfo = computed<boolean>(() => {
  return infoContent.value.length > 0;
});
</script>

<template>
  <div v-loading="stale" class="graph-player">
    <Transition>
      <div v-if="playerState === PlayerState.Start">
        <Intro />
      </div>
    </Transition>

    <!-- pop up wrapper -->
    <div class="data-popups">
      <DataPopups />
    </div>

    <Transition>
      <div v-if="playerState === PlayerState.Start && hasInfo" class="info">
        <Content :text="infoContent" />
      </div>
    </Transition>

    <Transition>
      <div v-if="playerState === PlayerState.Playing" class="audio-visualizer">
        <PlayerVisualizer />
      </div>
    </Transition>

    <Transition>
      <div v-if="playerState === PlayerState.Playing || playerState === PlayerState.End">
        <PlayerBar />
      </div>
    </Transition>

    <Transition>
      <div v-if="playerState === PlayerState.End">
        <EndScreen />
      </div>
    </Transition>

    <Transition>
      <div v-if="showInfo">
        <AudioInfo />
      </div>
    </Transition>

    <div v-if="data?.streamInfo.__typename === 'StreamInfo'">
      <Player ref="playerRef" :stream-point="data.streamInfo.stream.streamPoint" :stream="data.streamInfo.stream" />
      <ElCollapse v-if="showDebug" v-model="accorrdionNamespaceOpen" style="margin-top: 100px;">
        <ElCollapseItem title="Debug info" name="debug">
          <StreamInfo :stream="data.streamInfo.stream" :stream-instruction="data.streamInfo.streamInstruction" />
        </ElCollapseItem>
      </ElCollapse>
    </div>
    <div v-if="data?.streamInfo.__typename === 'NoStreamAvailable'">
      Currently no stream is available, please come back later.
    </div>
    <div v-if="error">
      Error: {{ error }}
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

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

.info {
  margin-bottom: $spacingXL;
}
</style>
