<script setup lang="ts">
import { type Ref, computed, nextTick, ref } from "vue";
import { ElCollapse, ElCollapseItem, ElMessage } from "element-plus";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";

import Player from "@/components/Player.vue";
import PlayerVisualizer from "@/components/PlayerVisualizer/PlayerVisualizer.vue";
import PlayerBar from "@/components/PlayerBar/PlayerBar.vue";
import StreamInfo from "@/components/StreamInfo.vue";
import EndScreen from "@/components/EndScreen.vue";
import MetaDialog from "@/components/Dialogs/MetaDialog.vue";
import Intro from "@/components/Intro.vue";
import IntroInfo from "@/components/IntroInfo.vue";

import type { UserDataRequest } from "@/models";
import { DrifterStatus, PlayerState, UserDataRequestType } from "@/models";
import { type Graph, useSendStreamVariableMutation, useStreamSubscription } from "@/graphql";
import { usePlayerStore } from "@/stores/Player";

const props = defineProps<{
  graph: Pick<Graph, "uuid" | "name" | "aboutText" | "displayName" | "startText" | "endText" | "slugName">
}>();

const {
  playerState,
  play,
  startingTimestamp
} = storeToRefs(usePlayerStore());

const router = useRouter();
// const showDebug = computed<boolean>(() => router.currentRoute.value.query.debug === null);
const showDebug: Ref<boolean> = ref(true);

const { data, error, stale } = useStreamSubscription({
  variables: {
    graphUuid: props.graph.uuid
  },
  pause: (router.currentRoute.value.name !== "graphPlayer") || (!props.graph.uuid)
});

const drifterStatus: Ref<DrifterStatus> = ref(DrifterStatus.WaitForStart);

const activeAccordionTab: Ref<string> = ref("");

const sendStreamVariableMutation = useSendStreamVariableMutation();

const startStream = async () => {
  if (data.value?.streamInfo.__typename === "NoStreamAvailable") {
    ElMessage.error("Can not start an unassigned stream");
    return;
  }
  const { error } = await sendStreamVariableMutation.executeMutation({
    streamVariables: {
      streamUuid: data.value?.streamInfo.stream.uuid,
      key: "start",
      value: "1.0",
      streamToSc: true
    }
  });
  if (error) {
    ElMessage.error(`Something went wrong ${error.message}`);
    return;
  }
  play.value = true;
  playerState.value = PlayerState.Playing;
  startingTimestamp.value = new Date().getTime();
  drifterStatus.value = DrifterStatus.WaitForUserInput;
};

// @todo how to figure out if our subscription is finished?
const dialogsToShow: Ref<UserDataRequest[]> = ref<UserDataRequest[]>([
  {
    name: "askGps",
    description: "Drifter ist ein dynamisches Hörspiel, das in Echtzeit generiert wird. Hierfür werden noch Informationen über dich benötigt:",
    key: "gps",
    type: UserDataRequestType.Gps,
    placeholder: ""
  },
  {
    name: "askName",
    description: "What would you like to be called?",
    key: "name",
    type: UserDataRequestType.String,
    placeholder: "Your name"
  },
  {
    name: "askName",
    description: "Please enter your name 2.",
    key: "name",
    type: UserDataRequestType.String,
    placeholder: "Your name"
  }
]);

const renderDialog = ref(true);

// we need short delays
const shiftDialogs = () => {
  if (dialogsToShow.value.length > 0) {
    // toggle renderDialog to re-render next dialog
    renderDialog.value = false;
    dialogsToShow.value.shift();
    nextTick(() => {
      renderDialog.value = true;
    });
  }
};
</script>

<template>
  <div class="drifter-graph-detail">
    <div v-loading="stale" class="graph-player">
      <!-- error handling -->
      <div v-if="data?.streamInfo.__typename === 'NoStreamAvailable'">
        Sorry, no stream available. Come back later.
      </div>
      <div v-else-if="!data">
        Some error :/
        Data is empty: {{ data }}
        Error: {{ error }}
      </div>
      <div v-else>
        <!-- start screen -->
        <Transition>
          <div v-if="drifterStatus === DrifterStatus.WaitForStart">
            <Intro
              :title="graph.displayName"
              :description-text="graph.startText"
              button-text="Start"
              @button-clicked="startStream()"
            />
            <div v-if="graph.aboutText">
              <IntroInfo
                :text="graph.aboutText"
              />
            </div>
          </div>
        </Transition>

        <!-- end screen -->
        <Transition>
          <div v-if="drifterStatus === DrifterStatus.ShowEndScreen">
            <EndScreen
              :text="graph.endText"
            />
          </div>
        </Transition>

        <!-- modals -->
        <div v-if="drifterStatus === DrifterStatus.WaitForUserInput">
          <div v-if="dialogsToShow[0] && renderDialog">
            <MetaDialog
              :request="dialogsToShow[0]"
              :stream-uuid="data.streamInfo.stream.uuid"
              @submitted="() => shiftDialogs()"
            />
          </div>
        </div>

        <!-- player -->
        <div v-if="data">
          <Player
            :stream-point="data.streamInfo.stream.streamPoint"
            :stream="data.streamInfo.stream"
          />
        </div>

        <!-- audio visualizer -->
        <Transition>
          <div v-if="playerState === PlayerState.Playing" class="audio-visualizer">
            <PlayerVisualizer />
          </div>
        </Transition>

        <!-- player bar -->
        <Transition>
          <div v-if="playerState === PlayerState.Playing || playerState === PlayerState.End">
            <PlayerBar
              :graph="graph"
              @clicked-stop="drifterStatus = DrifterStatus.ShowEndScreen"
            />
          </div>
        </Transition>

        <!-- debug -->
        <div v-if="showDebug" class="debug-wrapper">
          <ElCollapse
            v-model="activeAccordionTab"
          >
            <ElCollapseItem title="Debug info" name="debug">
              <StreamInfo
                :stream="data.streamInfo.stream"
                :stream-instruction="data.streamInfo.streamInstruction"
              />
            </ElCollapseItem>
          </ElCollapse>
        </div>
      </div>
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

.debug-wrapper {
  position: fixed;
  z-index: 0;
  width: 100%;
  height: auto;
  padding-left: 20px;
  padding-right: 20px;
  box-sizing: border-box;
  top: 120px;
  left: 0px;
}
</style>
