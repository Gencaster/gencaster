<script setup lang="ts">
import { type Ref, nextTick, ref, computed } from "vue";
import { ElCollapse, ElCollapseItem, ElMessage, ElImage } from "element-plus";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";

import Player from "@/components/PlayerComponent.vue";
import PlayerVisualizer from "@/components/PlayerVisualizer/PlayerVisualizer.vue";
import PlayerBar from "@/components/PlayerBar/PlayerBar.vue";
import StreamInfo from "@/components/StreamInfo.vue";
import EndScreen from "@/components/EndScreen.vue";
import MetaDialog from "@/components/Dialogs/MetaDialog.vue";
import Intro from "@/components/IntroCard.vue";
import IntroInfo from "@/components/IntroInfo.vue";

import type { UserDataRequest } from "@/models";
import { DrifterStatus, PlayerState, UserDataRequestType } from "@/models";
import {
  type Graph,
  useSendStreamVariableMutation,
  useStreamSubscription,
} from "@/graphql";
import { usePlayerStore } from "@/stores/Player";

const props = defineProps<{
  graph: Pick<
    Graph,
    | "uuid"
    | "name"
    | "aboutText"
    | "displayName"
    | "startText"
    | "endText"
    | "slugName"
  >;
}>();

const { playerState, play, startingTimestamp, playerMounted } = storeToRefs(
  usePlayerStore(),
);

const router = useRouter();
const showDebug = computed<boolean>(
  () => router.currentRoute.value.query.debug === null,
);
// const showDebug: Ref<boolean> = ref(true);

const { data, error, stale } = useStreamSubscription({
  variables: {
    graphUuid: props.graph.uuid,
  },
  pause: router.currentRoute.value.name !== "graphPlayer" || !props.graph.uuid,
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
      streamToSc: true,
    },
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
    description:
      "Walking Along a Sonic Möbius Strip ist eine ortsspezifische Komposition, welche in Echtzeit generiert wird. Hierfür ist der Zugriff auf den Standort erforderlich",
    key: "gps",
    type: UserDataRequestType.Gps,
    placeholder: "",
  },
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

const waitingTimeout = ref(false);

const showLoading = computed<boolean>(() => {
  if (stale.value) {
    return true;
  } else if (!playerMounted.value) {
    return true;
  } else {
    return false;
  }
});

const showError = computed<boolean>(() => {
  if (
    waitingTimeout.value &&
    (!data.value ||
      data.value?.streamInfo.__typename === "NoStreamAvailable" ||
      data.value.streamInfo.stream.streamPoint === undefined)
  ) {
    return true;
  } else {
    return false;
  }
});

const clickedStop = async () => {
  drifterStatus.value = DrifterStatus.ShowEndScreen;

  if (data.value?.streamInfo.__typename === "NoStreamAvailable") {
    return;
  }
  if (!data.value) {
    return;
  }
  const { error } = await sendStreamVariableMutation.executeMutation({
    streamVariables: {
      streamUuid: data.value.streamInfo.stream.uuid,
      key: "stop",
      value: "1.0",
      streamToSc: true,
    },
  });
};

// wait 3 seconds before showing error
setTimeout(() => {
  waitingTimeout.value = true;
}, 3000);
</script>

<template>
  <div class="drifter-graph-detail">
    <!-- error handling -->
    <div
      v-if="showError"
      class="error general-padding"
    >
      <div v-if="data?.streamInfo.__typename === 'NoStreamAvailable'">
        <p>
          Sorry, no stream available right now. Please come back later. <br>
          In case this error persists, please contact us
          <a href="mailto:contact@gencaster.org">here</a>.
        </p>
      </div>
      <div v-else-if="!data">
        Some error :/ Data is empty: {{ data }} Error: {{ error }}
      </div>
    </div>
    <div
      v-loading="showLoading"
      class="graph-player"
    >
      <div v-if="data?.streamInfo.__typename === 'StreamInfo'">
        <!-- start screen -->
        <Transition>
          <div
            v-if="drifterStatus === DrifterStatus.WaitForStart && playerMounted"
          >
            <Intro
              :title="graph.displayName"
              :description-text="graph.startText"
              button-text="Start"
              @button-clicked="startStream()"
            />
            <div v-if="graph.aboutText">
              <IntroInfo :text="graph.aboutText" />
            </div>
          </div>
        </Transition>

        <!-- end screen -->
        <Transition>
          <div v-if="drifterStatus === DrifterStatus.ShowEndScreen">
            <EndScreen :text="graph.endText" />
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
        <div v-if="data.streamInfo.stream">
          <Player
            :stream-point="data.streamInfo.stream.streamPoint"
            :stream="data.streamInfo.stream"
          />
        </div>

        <!-- audio visualizer -->
        <Transition>
          <div
            v-if="playerState === PlayerState.Playing"
            class="audio-visualizer"
          >
            <PlayerVisualizer />
            <center>
              <ElImage
                src="https://hedgedoc.musikinformatik.net/uploads/a403e2d4-bde1-4ed2-9a74-9331e45ccf63.png"
                style="max-width: 900px"
                fit="contain"
              />
            </center>
          </div>
        </Transition>

        <!-- player bar -->
        <Transition>
          <div
            v-if="
              playerState === PlayerState.Playing ||
                playerState === PlayerState.End
            "
          >
            <PlayerBar
              :graph="graph"
              @clicked-stop="clickedStop()"
            />
          </div>
        </Transition>

        <!-- debug -->
        <div
          v-if="showDebug"
          class="debug-wrapper"
        >
          <ElCollapse v-model="activeAccordionTab">
            <ElCollapseItem
              title="Debug info"
              name="debug"
            >
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
@import "@/assets/mixins.scss";
@import "@/assets/variables.scss";

.graph-player {
  min-height: 100vh;
  max-height: 100vh;
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
