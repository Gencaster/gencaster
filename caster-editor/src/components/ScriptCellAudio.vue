<template>
  <div class="block">
    <p @click="showBrowser = true">
      This is the audio Block
      {{ scriptCell.audioCell.audioFile.uuid }}
    </p>
    <Browser
      v-if="showBrowser"
      @cancel="showBrowser = false"
      @selected-audio-file="(uuid) => {
        audioFileUUID=uuid;
        showBrowser=false;
      }"
    />
  </div>
</template>

<script lang="ts" setup>
import type { ScriptCell, AudioCell, AudioFile, DjangoFileType
 } from "@/graphql";

export interface AudioFileURL extends Pick<AudioFile, 'uuid'> {
  file: Pick<DjangoFileType, 'url'>
}

export interface AudioCellData extends Pick<AudioCell, 'playback' | 'uuid'> {
  audioFile: AudioFileURL
}

export interface AudioScriptCellData extends Pick<ScriptCell, 'cellCode' | 'cellType'> {
    audioCell: AudioCellData
}

import Browser from "@/components/AudioFileBrowser.vue";
import { computed, ref, type Ref  } from "vue";

const props = defineProps<{
    text: string,
}>();
const emit = defineEmits<{
  (e: "update:scriptCell", scriptCell: AudioScriptCellData): void
}>();

const showBrowser: Ref<boolean> = ref(false);

const audioFileUUID = computed({
    get() {
        return props.scriptCell.audioCell.uuid;
    },
    set(value) {
        console.log("Hello from BlockAudio", value);
        const updatedModel = {...props.scriptCell};
        if (updatedModel.audioCell) {
            updatedModel.audioCell.audioFile.uuid = value;
        }
        emit('update:scriptCell', updatedModel);
        return value
    }
});
</script>
