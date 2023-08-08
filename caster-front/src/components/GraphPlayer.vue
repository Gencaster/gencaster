<script setup lang="ts">
import { type Ref, ref, computed, watch, reactive } from "vue";
import {
  ElButton,
  ElCheckbox,
  ElCollapse,
  ElCollapseItem,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElMessage,
} from "element-plus";
import { useRouter } from "vue-router";
import Player from "@/components/PlayerComponent.vue";
import {
  type Graph,
  type StreamSubscription,
  ButtonType,
  type Button,
  CallbackAction,
  type StreamVariableInput,
  type Checkbox,
} from "@/graphql";
import { useStreamSubscription } from "@/graphql";
import StreamInfo from "@/components/StreamInfo.vue";
import PlayerButtons from "@/components/PlayerButtons.vue";
import { useSendStreamVariableMutation } from "@/graphql";
import { storeToRefs } from "pinia";
import { usePlayerStore } from "@/stores/Player";

import Intro from "@/components/IntroCard.vue";
import IntroInfo from "@/components/IntroInfo.vue";
import { PlayerState } from "@/models";
import PlayerVisualizer from "@/components/PlayerVisualizer/PlayerVisualizer.vue";
import PlayerBar from "@/components/PlayerBar/PlayerBar.vue";
import EndScreen from "@/components/EndScreen.vue";

interface DialogShow {
  show: boolean;
  loading: boolean;
  dialog: Extract<StreamSubscription["streamInfo"], { __typename: "Dialog" }>;
}

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
  showDebug?: boolean;
}>();

const {
  streamGPS,
  gpsError,
  gpsSuccess,
  playerState,
  play,
  startingTimestamp,
  playerMounted,
} = storeToRefs(usePlayerStore());

const router = useRouter();

const sendStreamVariable = useSendStreamVariableMutation();

const showDialog: Ref<boolean> = ref(true);
const dialogsToShow: Ref<DialogShow[]> = ref([]);

const streamInfo: Ref<
  | Extract<StreamSubscription["streamInfo"], { __typename: "StreamInfo" }>
  | undefined
> = ref(undefined);
const streamError: Ref<
  | Extract<
      StreamSubscription["streamInfo"],
      { __typename: "NoStreamAvailable" }
    >
  | undefined
> = ref(undefined);

const currentDialog = computed<DialogShow | undefined>(() => {
  if (dialogsToShow.value.length < 1) {
    return undefined;
  }
  return dialogsToShow.value[0];
});

// send a start variable when the client is connected to a stream
watch(streamInfo, (info) => {
  if (info) {
    sendStreamVariable.executeMutation({
      streamVariables: [
        {
          streamUuid: info.stream.uuid,
          key: "ready",
          value: "1.0",
          streamToSc: true,
        },
      ],
    });
  }
});

const { error, stale } = useStreamSubscription(
  {
    variables: {
      graphUuid: props.graph.uuid,
    },
    pause: router.currentRoute.value.name !== "graphPlayer",
  },
  (oldInfo, newInfo) => {
    // as the subscription switches between different types it is necessary
    // to cache the intermediate results as otherwise the player would reconnect
    // on every change.
    if (newInfo.streamInfo.__typename === "Dialog") {
      dialogsToShow.value.push({
        dialog: newInfo.streamInfo,
        show: true,
        loading: false,
      });
    } else if (newInfo.streamInfo.__typename === "StreamInfo") {
      streamInfo.value = newInfo.streamInfo;
    }
    return newInfo;
  },
);

const closedDialog = () => {
  if (currentDialog.value) {
    currentDialog.value.loading = false;
  }
  setTimeout(() => {
    dialogsToShow.value.shift();
    if (currentDialog.value) {
      showDialog.value = true;
    }
  }, 100);
};

let formData: Record<string, any> = reactive<Record<string, any>>({});

const playerRef: Ref<InstanceType<typeof Player> | undefined> = ref(undefined);

const closeCurrentDialog = () => {
  formData = reactive<Record<string, any>>({});
  if (currentDialog.value) {
    currentDialog.value.loading = false;
    currentDialog.value.show = false;
  }
};

// gps stuff
watch(gpsSuccess, () => {
  console.log("Received first GPS signal - connection successful");
  closeCurrentDialog();
});

watch(gpsError, () => {
  if (gpsError.value) {
    console.log(
      `Error at obtaining GPS handle: ${gpsError.value}`,
      gpsError.value,
    );
    if (gpsError.value.PERMISSION_DENIED) ElMessage.error("Plesae allow GPS.");
    else if (
      gpsError.value.POSITION_UNAVAILABLE ||
      gpsError.value.PERMISSION_DENIED
    )
      ElMessage.error(
        `Could not obtain a GPS position: ${gpsError.value.message}`,
      );
    router.push("/gps-error");
  }
});

const setupGPS = async () => {
  if (gpsSuccess.value) {
    // gps is already running so nothing to do
    closeCurrentDialog();
  }
  // as it makes only sense to have one GPS stream we refer to
  // it via the global store.
  streamGPS.value = true;
  // a watcher which checks the status of the GPS request
  const refreshIntervalId = setInterval(async () => {
    // i don't have a clue if this works properly b/c I always receive a GPS location first
    // but "in theory" it should also help us
    const { state } = await navigator.permissions.query({
      name: "geolocation",
    });
    console.log("state is", state);
    if (state === "granted") {
      gpsSuccess.value = true;
      clearInterval(refreshIntervalId);
      closeCurrentDialog();
    }
  }, 100);
};

// callback stuff
const processAction = async (button: Button | Checkbox) => {
  if (!streamInfo.value) {
    console.log(
      `Can not send stream variable ${sendStreamVariable} because stream info is missing`,
    );
    return;
  }
  if (currentDialog.value) {
    currentDialog.value.loading = true;
  }
  let gpsAction = false;
  const updates: StreamVariableInput[] = [];
  button.callbackActions.forEach((action) => {
    if (action === CallbackAction.SendVariable) {
      updates.push({
        streamUuid: streamInfo.value?.stream.uuid,
        key: button.key,
        value: "value" in button ? button.value : String(button.checked),
      });
    }

    if (action === CallbackAction.SendVariables) {
      Object.keys(formData).forEach((key) => {
        updates.push({
          streamUuid: streamInfo.value?.stream.uuid,
          key: key,
          value: formData[key],
        });
      });
    }

    if (action === CallbackAction.ActivateGpsStreaming) {
      gpsAction = true;
    }
  });

  if (updates.length > 0) {
    const { error } = await sendStreamVariable.executeMutation({
      streamVariables: updates,
    });
    if (error) {
      ElMessage.error(
        `Could not transfer variable to server: ${error.message}`,
      );
    }
  }

  if (gpsAction) {
    setupGPS();
    return;
  }

  // reset form data
  formData = reactive<Record<string, any>>({});
  if (currentDialog.value) {
    currentDialog.value.loading = false;
    currentDialog.value.show = false;
  }
};

enum ElButtonType {
  Danger = "danger",
  Default = "default",
  Info = "info",
  Primary = "primary",
  Success = "success",
  Warning = "warning",
}
// helper function which maps graphql ButtonType enum to ElButtonType enum
const convertButtonType = (b: ButtonType): ElButtonType => {
  switch (b) {
    case ButtonType.Danger:
      return ElButtonType.Danger;
    case ButtonType.Default:
      return ElButtonType.Default;
    case ButtonType.Info:
      return ElButtonType.Info;
    case ButtonType.Primary:
      return ElButtonType.Primary;
    case ButtonType.Success:
      return ElButtonType.Success;
    case ButtonType.Warning:
      return ElButtonType.Warning;
    default:
      return ElButtonType.Default;
  }
};

const sendStreamVariableMutation = useSendStreamVariableMutation();

// template functions
const startStream = async () => {
  // TODO: Do we still need this?
  // I don't think so, since the page should show an error if it can't get a stream
  // if (data.value?.streamInfo.__typename === "NoStreamAvailable") {
  //   ElMessage.error("Can not start an unassigned stream");
  //   return;
  // }
  const { error } = await sendStreamVariableMutation.executeMutation({
    streamVariables: {
      streamUuid: streamInfo.value?.stream.uuid,
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
};
</script>

<template>
  <div
    v-loading="stale"
    class="graph-player"
  >
    <div v-if="currentDialog">
      <ElDialog
        v-model="currentDialog.show"
        v-loading="currentDialog.loading"
        :title="currentDialog.dialog.title"
        :append-to-body="true"
        :close-on-click-modal="false"
        :show-close="false"
        @closed="closedDialog()"
      >
        <ElForm label-position="top">
          <span
            v-for="(content, index) in currentDialog.dialog.content"
            :key="index"
          >
            <div v-if="content.__typename == 'Text'">
              <span>
                {{ content.text }}
              </span>
            </div>
            <div v-if="content.__typename == 'Checkbox'">
              <ElFormItem
                v-model="formData[content.key]"
                :label="content.label"
                @click="processAction(content)"
              >
                <ElCheckbox />
              </ElFormItem>
            </div>
            <div v-if="content.__typename == 'Input'">
              <ElFormItem :label="content.label">
                <ElInput
                  v-model="formData[content.key]"
                  :placeholder="content.placeholder"
                />
              </ElFormItem>
            </div>

            <br>
          </span>
        </ElForm>
        <template #footer>
          <span class="dialog-footer">
            <ElButton
              v-for="(button, index) in currentDialog.dialog.buttons"
              :key="index"
              :type="convertButtonType(button.buttonType)"
              @click="processAction(button)"
            >
              {{ button.text }}
            </ElButton>
          </span>
        </template>
      </ElDialog>
    </div>
    <div v-if="streamInfo">
      <!-- start screen -->
      <Transition>
        <div v-if="playerMounted && playerState === 'start'">
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

      <!-- audio visualizer -->
      <Transition>
        <div
          v-if="playerState === PlayerState.Playing"
          class="audio-visualizer"
        >
          <PlayerVisualizer />
        </div>
      </Transition>

      <!-- player bar -->
      <Transition>
        <div v-if="playerState === PlayerState.Playing">
          <PlayerBar
            :graph="graph"
            @clicked-stop="playerState = PlayerState.End"
          />
        </div>
      </Transition>

      <!-- end screen -->
      <Transition>
        <div v-if="playerState === PlayerState.End">
          <EndScreen :text="graph.endText" />
        </div>
      </Transition>

      <!-- <PlayerButtons /> -->
      <Player
        ref="playerRef"
        :stream-point="streamInfo.stream.streamPoint"
        :stream="streamInfo.stream"
      />
      <ElCollapse
        v-if="showDebug"
        class="debug-info-wrapper"
      >
        <ElCollapseItem title="Debug info">
          <StreamInfo
            :stream="streamInfo.stream"
            :stream-instruction="streamInfo.streamInstruction"
          />
        </ElCollapseItem>
      </ElCollapse>
    </div>
    <div v-if="streamError">
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
</style>
