<template>
  <div class="block">
    <p @click="showBrowser = true">
      This is the audio Block {{ audioCell.audioFile.uuid }}
    </p>
    <p>
      <ElSelect
        v-model="audioCellData.playback"
        placeholder="Select"
      >
        <ElOption
          v-for="item in Object.keys(PlaybackChoices)"
          :key="item"
          :label="item"
          :value="item"
        />
      </ElSelect>
    </p>
    <p>
      <ElSlider
        v-model="audioCellData.volume"
        :min="0.0"
        :max="1.0"
        :step="0.01"
        show-input
      />
    </p>
    <Browser
      v-if="showBrowser"
      @cancel="showBrowser = false"
      @selected-audio-file="(uuid) => {
        audioCellData.audioFile.uuid = uuid;
        showBrowser=false;
      }"
    />
  </div>
</template>

<script lang="ts" setup>
import { type ScriptCell, type AudioCell, type AudioFile, type DjangoFileType, PlaybackChoices
 } from "@/graphql";

export interface AudioFileURL extends Pick<AudioFile, 'uuid'> {
  file: Pick<DjangoFileType, 'url'>
}

export interface AudioCellData extends Pick<AudioCell, 'playback' | 'uuid' | 'volume'> {
  audioFile: AudioFileURL
}

export interface AudioScriptCellData extends Pick<ScriptCell, 'cellCode' | 'cellType'> {
    audioCell: AudioCellData
}

import Browser from "@/components/AudioFileBrowser.vue";
import { computed, ref, type Ref  } from "vue";
import { ElSelect, ElOption, ElSlider } from "element-plus";

const props = defineProps<{
    text: string,
    audioCell: AudioCellData
}>();

const emit = defineEmits<{
  (e: "update:audioCell", scriptCell: AudioCellData): void
  (e: "update:text", text: string): void
}>();

const showBrowser: Ref<boolean> = ref(false);

const audioCellData = computed<AudioCellData>({
  get() {
    return props.audioCell
  },
  set(value) {
    emit('update:audioCell', value);
    return value;
  }
});

</script>
