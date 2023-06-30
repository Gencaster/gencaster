<script setup lang="ts">
import { type Ref, ref, computed } from "vue";
import { ElCollapse, ElCollapseItem, ElDialog } from "element-plus";
import { useRouter } from "vue-router";
import Player from "@/components/PlayerComponent.vue";
import type { Dialog, Graph } from "@/graphql";
import { useStreamSubscription } from "@/graphql";
import StreamInfo from "@/components/StreamInfo.vue";
import PlayerButtons from "@/components/PlayerButtons.vue";

const props = defineProps<{
  graph: Pick<Graph, "uuid" | "name">;
}>();

const router = useRouter();

const dialogsToShow: Ref<Dialog[]> = ref([]);

const showDialog: Ref<boolean> = ref(true);

const currentDialog = computed<Dialog | undefined>(() => {
  return dialogsToShow.value[0];
});

const { data, error, stale } = useStreamSubscription(
  {
    variables: {
      graphUuid: props.graph.uuid,
    },
    pause: router.currentRoute.value.name !== "graphPlayer",
  },
  (oldInfo, newInfo) => {
    if (newInfo.streamInfo.__typename === "Dialog") {
      dialogsToShow.value.push(newInfo.streamInfo);
    }
    return newInfo;
  },
);

const playerRef: Ref<InstanceType<typeof Player> | undefined> = ref(undefined);
</script>

<template>
  <div
    v-loading="stale"
    class="graph-player"
  >
    <h2>{{ graph.name }}</h2>
    <div v-if="currentDialog">
      <ElDialog
        v-model="showDialog"
        :title="currentDialog.title"
      >
        {{ currentDialog.content.text }}
      </ElDialog>
    </div>
    <div v-if="data?.streamInfo.__typename === 'StreamInfo'">
      <PlayerButtons />
      <Player
        ref="playerRef"
        :stream-point="data.streamInfo.stream.streamPoint"
        :stream="data.streamInfo.stream"
      />
      <ElCollapse class="debug-info-wrapper">
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

<style lang="scss" scoped>
@import "@/assets/mixins.scss";
@import "@/assets/variables.scss";

.debug-info-wrapper {
  margin-top: 10px;
}
</style>
