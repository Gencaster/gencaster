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
          :audio-file="audioCell.audioFile as AudioType"
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
        <ScriptCellMarkdown
          v-model:text="textData"
          :cell-type="CellType.Comment"
        />
      </div>
    </div>

    <Browser
      v-if="showBrowser"
      @cancel="showBrowser = false"
      @selected-audio-file="(uuid: Scalars['UUID']) => {
        audioCellData.audioFile.uuid = uuid;
        showBrowser = false;
      }"
    />
  </div>
</template>

<script lang="ts" setup>
import { computed, ref, type Ref } from "vue";
import Browser from "@/components/AudioFileBrowser.vue";
import AudioPlayer, { type AudioType } from "./AudioFilePlayer.vue"
import ScriptCellMarkdown from './ScriptCellMarkdown.vue';
import { ElSelect, ElOption, ElSlider } from "element-plus";
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { type ScriptCell, type AudioCell, type AudioFile, PlaybackChoices, type Scalars } from "@/graphql";
import { CellType } from "@/graphql";


// Props and Types
type AudioScriptCellData = Pick<ScriptCell, 'cellCode' | 'cellType'> & {
  audioCell: Pick<AudioCell, 'uuid' | 'volume' | 'playback'> & {
    audioFile: AudioFile
  }
}

const props = defineProps<{
  text: string,
  audioCell: AudioScriptCellData['audioCell']
}>();

// Mutations
const emit = defineEmits<{
  (e: "update:audioCell", scriptCell: AudioScriptCellData['audioCell']): void
  (e: "update:text", text: string): void
}>();

const audioCellData = computed<AudioScriptCellData['audioCell']>({
  get() {
    return props.audioCell
  },
  set(value) {
    console.log('current audio cell internal', value);
    emit('update:audioCell', value);
    return value;
  }
});

const textData = computed<string>({
  get() {
    return props.text;
  },
  set(value) {
    emit('update:text', value);
    return value;
  }
});

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
