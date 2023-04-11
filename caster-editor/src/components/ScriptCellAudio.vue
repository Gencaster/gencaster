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
          v-for="[key, value] in Object.entries(PlaybackChoices)"
          :key="key"
          :label="key"
          :value="value"
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
      @selected-audio-file="(uuid: Scalars['UUID']) => {
        audioCellData.audioFile.uuid = uuid;
        showBrowser=false;
      }"
    />
  </div>
</template>

<script lang="ts" setup>
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { type ScriptCell, type AudioCell, type AudioFile, PlaybackChoices, type Scalars} from "@/graphql";

import Browser from "@/components/AudioFileBrowser.vue";
import { computed, ref, type Ref  } from "vue";
import { ElSelect, ElOption, ElSlider } from "element-plus";

type AudioScriptCellData = Pick<ScriptCell, 'cellCode' | 'cellType'> & {
    audioCell: Pick<AudioCell, 'uuid' | 'volume' | 'playback'> & {
      audioFile: Pick<AudioFile, 'uuid'> & {
        // file: null | undefined | Pick<DjangoFileType, 'url'>
      }
    }
}

const props = defineProps<{
    text: string,
    audioCell: AudioScriptCellData['audioCell']
}>();

const emit = defineEmits<{
  (e: "update:audioCell", scriptCell: AudioScriptCellData['audioCell']): void
  (e: "update:text", text: string): void
}>();

const showBrowser: Ref<boolean> = ref(false);

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

</script>
