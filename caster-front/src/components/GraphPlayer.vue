<script setup lang="ts">
import { type Ref, computed, ref } from "vue";
import { ElButton, ElCollapse, ElCollapseItem } from "element-plus";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import Player from "@/components/Player.vue";
import GraphPlayerCredits from "@/components/GraphPlayerCredits.vue";
import PlayerVisualizer from "@/components/PlayerVisualizer/PlayerVisualizer.vue";
import PlayerBar from "@/components/PlayerBar/PlayerBar.vue";
import StreamInfo from "@/components/StreamInfo.vue";
import EndScreen from "@/components/EndScreen.vue";
import Content from "@/components/Content.vue";
import DataPopups from "@/components/DataPopups.vue";
import AudioInfo from "@/components/AudioInfo.vue";

import type { Graph } from "@/graphql";
import { useStreamSubscription } from "@/graphql";
import { usePlayerStore } from "@/stores/Player";
const props = defineProps<{
  graph: Pick<Graph, "uuid" | "name">
}>();

const {
  play,
  startingTimestamp,
  playerState,
  title,
  description,
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

const debugOpen = "debug";
const playerRef: Ref<InstanceType<typeof Player> | undefined> = ref(undefined);

const hasInfo = computed<boolean>(() => {
  return infoContent.value.length > 0;
});

const startListening = () => {
  play.value = true;
  playerState.value = "playing";
  startingTimestamp.value = new Date().getTime();
};
</script>

<template>
  <div v-loading="stale" class="graph-player">
    <Transition>
      <div v-if="playerState === 'start'">
        <div class="fullscreen-wrapper-relative">
          <div class="graph-title-card">
            <h1 class="title">
              {{ title }}
            </h1>
            <p class="description">
              {{ description }}
            </p>
            <div class="button-wrapper">
              <ElButton class="caps green" size="large" type="default" @click="startListening()">
                Start
              </ElButton>
            </div>
          </div>
          <GraphPlayerCredits />
        </div>
      </div>
    </Transition>

    <!-- pop up wrapper -->
    <!-- <div v-if="playerState === 'playing'" class="data-popups"> -->
    <div class="data-popups">
      <DataPopups />
    </div>

    <Transition>
      <div v-if="playerState === 'start' && hasInfo" class="info">
        <Content :text="infoContent" />
      </div>
    </Transition>

    <Transition>
      <div v-if="playerState === 'playing'" class="audio-visualizer">
        <PlayerVisualizer />
      </div>
    </Transition>

    <Transition>
      <div v-if="playerState === 'playing' || playerState === 'end'">
        <PlayerBar :title="title" />
      </div>
    </Transition>

    <Transition>
      <div v-if="playerState === 'end'">
        <EndScreen />
      </div>
    </Transition>

    <Transition>
      <div v-if="showInfo">
        <AudioInfo />
      </div>
    </Transition>

    <div v-if="data?.streamInfo.__typename === 'StreamInfo'">
      <Player
        ref="playerRef"
        :stream-point="data.streamInfo.stream.streamPoint"
        :stream="data.streamInfo.stream"
      />
      <ElCollapse v-if="showDebug" v-model="debugOpen" style="margin-top: 100px;">
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

.graph-player {
  z-index: 1;
  padding-left: $mobilePadding;
  padding-right: $mobilePadding;

  .graph-title-card {
    margin: 0 auto;
    position: relative;
    display: block;
    box-sizing: border-box;
    border-radius: $borderRadius;
    border: $lineStandard solid $black;
    padding: 20px;
    background-color: $white;
    width: calc(100% - 2 * $mobilePadding);
    max-width: $cardMaxWidth;

    .title {
      margin-top: 0px;
      text-align: center;
    }

    .description {
      text-align: center;
      margin-bottom: calc($spacingM * 3);
      @include fontStyle('smallHeadline');
    }

    .button-wrapper {
      position: absolute;
      width: 100%;
      display: flex;
      justify-content: center;
      left: 0;
      bottom: -30px;

      .el-button {
        display: inline-block;
      }
    }
  }
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

.info {
  margin-bottom: $spacingXL;
}
</style>
