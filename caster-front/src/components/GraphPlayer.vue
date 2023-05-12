<script setup lang="ts">
import { type Ref, ref } from "vue";
import { ElButton, ElCollapse, ElCollapseItem } from "element-plus";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import Player from "@/components/Player.vue";
import GraphPlayerCredits from "@/components/GraphPlayerCredits.vue";
import PlayerVisualizer from "@/components/PlayerVisualizer.vue";

import type { Graph } from "@/graphql";
import { useStreamSubscription } from "@/graphql";
import StreamInfo from "@/components/StreamInfo.vue";

import { usePlayerStore } from "@/stores/Player";
import PlayerButtons from "@/components/PlayerButtons.vue";
const props = defineProps<{
  graph: Pick<Graph, "uuid" | "name">
}>();

const { play } = storeToRefs(usePlayerStore());

const router = useRouter();

const { data, error, stale } = useStreamSubscription({
  variables: {
    graphUuid: props.graph.uuid
  },
  pause: router.currentRoute.value.name !== "graphPlayer"
});

const playerRef: Ref<InstanceType<typeof Player> | undefined> = ref(undefined);

const showTitle = ref(true);
</script>

<template>
  <div v-loading="stale" class="graph-player">
    <Transition>
      <div v-if="showTitle" class="fullscreen-wrapper">
        <div>
          <div class="graph-title-card">
            <h1 class="title">
              {{ graph.name }}
            </h1>
            <p class="description">
              Ein GPS basierter Audiowalk entlang des berühmten Wahrzeichens.
            </p>
            <div class="button-wrapper">
              <ElButton
                class="caps green" size="large" type="default" style="width: 100%;"
                @click="play = !play; showTitle = false"
              >
                Start
              </ElButton>
            </div>
          </div>
        </div>

        <GraphPlayerCredits />
      </div>
    </Transition>

    <div class="audio-visualizer">
      <PlayerVisualizer />
    </div>

    <div v-if=" data?.streamInfo.__typename === 'StreamInfo' ">
      <Player ref="playerRef" :stream-point=" data.streamInfo.stream.streamPoint " :stream=" data.streamInfo.stream " />
      <ElCollapse style="margin-top: 10px;">
        <ElCollapseItem title="Debug info">
          <StreamInfo :stream=" data.streamInfo.stream " :stream-instruction=" data.streamInfo.streamInstruction " />
        </ElCollapseItem>
      </ElCollapse>
    </div>
    <div v-if=" data?.streamInfo.__typename === 'NoStreamAvailable' ">
      Currently no stream is available, please come back later.
    </div>
    <div v-if=" error ">
      Error: {{ error }}
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

.graph-player {
  .graph-title-card {
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
</style>
