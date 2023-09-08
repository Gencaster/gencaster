<template>
  <div class="block block-audio">
    <div class="audio-file slot half">
      <div class="header">
        <p class="title">
          {{ audioCell.audioFile.name }}
        </p>
        <p
          class="edit-button"
          @click="showBrowser = true"
        >
          edit
        </p>
      </div>
      <div class="content">
        <AudioPlayer
          :audio-file="audioCellData.audioFile"
          :type="'minimal'"
          :volume="audioCellData.volume"
        />
      </div>
    </div>
    <div class="playback slot quarter">
      <div class="header">
        <p class="title lighter">
          Playback
        </p>
      </div>
      <div class="content">
        <ElSelect
          v-model="audioCellData.playback"
          placeholder="Select"
        >
          <ElOption
            v-for="[key, value] in Object.entries(PlaybackChoices)"
            :key="key"
            :label="key"
            :value="value"
          />
        </ElSelect>
      </div>
    </div>
    <div class="volume slot quarter">
      <div class="header">
        <p class="title lighter">
          Volume
        </p>
      </div>

      <div class="content">
        <ElSlider
          v-model="audioCellData.volume"
          :min="0.0"
          :max="1.0"
          :step="0.01"
        />
      </div>
    </div>
    <div class="comment slot half">
      <div class="header">
        <p class="title lighter">
          Comment
        </p>
      </div>

      <div class="content">
        <!-- The markdown component takes care of any necessary text updates -->
        <ScriptCellMarkdown
          v-model:text="textData"
          :cell-type="CellType.Comment"
          :uuid="uuid"
        />
      </div>
    </div>

    <Browser
      v-if="showBrowser"
      @cancel="showBrowser = false"
      @selected-audio-file="
        (audioFile) => {
          audioCellData.audioFile.name = audioFile.name;
          audioCellData.audioFile.uuid = audioFile.uuid;
          if (audioCellData.audioFile.file?.url && audioFile.file) {
            audioCellData.audioFile.file.url = audioFile.file.url;
          }

          showBrowser = false;
        }
      "
    />
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, watch, type Ref, computed } from "vue";
import Browser from "@/components/AudioFileBrowser.vue";
import AudioPlayer from "./AudioFilePlayer.vue";
import ScriptCellMarkdown from "./ScriptCellMarkdown.vue";
import { ElSelect, ElOption, ElSlider } from "element-plus";
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import {
  type ScriptCell,
  type AudioCell,
  type AudioFile,
  PlaybackChoices,
  type DjangoFileType,
  type AudioCellInput,
} from "@/graphql";
import { CellType } from "@/graphql";
import { storeToRefs } from "pinia";
import { useInterfaceStore } from "@/stores/InterfaceStore";

// Props and Types

type Maybe<T> = T | undefined | null;

type AudioScriptCellData = Pick<ScriptCell, "cellCode" | "cellType"> & {
  audioCell: Pick<AudioCell, "uuid" | "volume" | "playback"> & {
    audioFile: Pick<AudioFile, "name" | "uuid"> & {
      file?: Maybe<Pick<DjangoFileType, "url">>;
    };
  };
};

const props = defineProps<{
  text: string;
  audioCell: AudioScriptCellData["audioCell"];
  uuid: string;
}>();

const { newScriptCellUpdates } = storeToRefs(useInterfaceStore());

const audioCellData = reactive<AudioScriptCellData["audioCell"]>({
  volume: props.audioCell.volume,
  uuid: props.audioCell.uuid,
  playback: props.audioCell.playback,
  audioFile: props.audioCell.audioFile,
});

// in case we receive an update of the props we also update the reactive component
// this is only necessary for playback and volume
// for some reason props is not reactive so we make it reactive
// by turning it into a computed property, probably an anti pattern
//
// we use a 'clutch' to discard incoming updates
// as updates of our own
const dataClutch = ref<boolean>(false);
watch(
  computed(() => props.audioCell),
  (newValue) => {
    dataClutch.value = true;
    audioCellData.playback = newValue.playback;
    audioCellData.volume = newValue.volume;
    // watch takes some time to keep up, so the clutch
    // needs to be on for some time
    setTimeout(() => {
      dataClutch.value = false;
    }, 10);
  },
  { deep: true },
);

watch(
  audioCellData,
  (newData) => {
    if (dataClutch.value) {
      // ignore updates from props update
      return;
    }
    let update = newScriptCellUpdates.value.get(props.uuid);

    const audioCellUpdate: AudioCellInput = {
      uuid: newData.uuid,
      audioFile: { uuid: audioCellData.audioFile.uuid },
      volume: audioCellData.volume,
      playback: audioCellData.playback,
    };

    if (update) {
      update.audioCell = audioCellUpdate;
    } else {
      newScriptCellUpdates.value.set(props.uuid, {
        uuid: props.uuid,
        audioCell: audioCellUpdate,
      });
    }
  },
  { deep: true },
);

const textData = ref<string>(props.text);

// State
const showBrowser: Ref<boolean> = ref(false);
</script>

<style lang="scss" scoped>
@import "@/assets/scss/variables.module.scss";

.block {
  display: flex;
  flex-direction: row;
  min-height: 90px;

  .slot {
    padding: 10px;
    display: flex;
    flex-direction: column;
  }

  .half {
    width: 50%;
  }

  .quarter {
    width: 25%;
  }

  .header {
    display: flex;
    justify-content: space-between;
    height: 20px;

    .lighter {
      color: $grey-dark;
    }

    p {
      margin: 0;
    }
  }

  .content {
    // background-color: yellow;
    height: 100%;
  }

  .audio-file {
    border-right: 1px solid $grey;
    background-color: white;

    .edit-button {
      cursor: pointer;
      font-style: italic;

      &:hover {
        text-decoration: underline;
      }
    }

    .content {
      display: flex;
      align-items: end;
      // justify-content: space-around;
      // align-items: flex-end;
    }
  }

  .playback,
  .volume {
    border-right: 1px solid $grey;

    .content {
      display: flex;
      align-items: end;
    }
  }

  .comment {
    .content {
      .block-markdown {
        min-height: 60px;
        margin: 0;
        padding: 0;
        width: 100%;

        :deep(.editor-comment) {
          width: 100%;
          .toastui-editor-defaultUI .ProseMirror {
            padding: 4px 0px 12px 0px;
            overflow-wrap: anywhere;
          }
        }
      }
    }
  }
}
</style>
