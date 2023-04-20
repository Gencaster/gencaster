<script setup lang="ts">
import { type Ref, ref } from "vue";
import { ElCollapse, ElCollapseItem } from "element-plus";
import { useRouter } from "vue-router";
import Player from "@/components/Player.vue";
import type { Graph } from "@/graphql";
import { useStreamSubscription } from "@/graphql";
import StreamInfo from "@/components/StreamInfo.vue";
import PlayerButtons from "@/components/PlayerButtons.vue";

const props = defineProps<{
  graph: Pick<Graph, "uuid" | "name">
}>();

const router = useRouter();

const { data, error, stale } = useStreamSubscription({
  variables: {
    graphUuid: props.graph.uuid
  },
  pause: router.currentRoute.value.name !== "graphPlayer"
});

const playerRef: Ref<InstanceType<typeof Player> | undefined> = ref(undefined);
</script>

<template>
  <div v-loading="stale" class="graph-player">
    <h2>{{ graph.name }}</h2>
    <div v-if="data?.streamInfo.__typename === 'StreamInfo'">
      <PlayerButtons />
      <Player
        ref="playerRef"
        :stream-point="data.streamInfo.stream.streamPoint"
        :stream="data.streamInfo.stream"
      />
      <ElCollapse style="margin-top: 10px;">
        <ElCollapseItem title="Debug info">
          <StreamInfo
            :stream="data.streamInfo.stream"
            :stream-instruction="data.streamInfo.streamInstruction"
          />
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
