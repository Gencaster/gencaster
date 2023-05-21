<!-- eslint-disable vue/no-mutating-props -->
<template>
  <div class="cell">
    <ScriptCellMarkdown
      v-if="scriptCell.cellType === CellType.Markdown || scriptCell.cellType === CellType.Comment"
      v-model:text="scriptCellText"
      :cell-type="scriptCell.cellType"
    />
    <ScriptCellCodemirror
      v-if="scriptCell.cellType === CellType.Python || scriptCell.cellType === CellType.Supercollider"
      v-model:text="scriptCellText"
      :cell-type="scriptCell.cellType"
    />
    <div v-if="scriptCell.audioCell!==undefined">
      <ScriptCellAudio
        v-if="scriptCell.audioCell !== undefined && scriptCell.audioCell !== null && scriptCell.audioCell?.audioFile.file !== undefined && scriptCell.cellType === CellType.Audio"
        v-model:text="scriptCellText"
        v-model:audio-cell="scriptCell.audioCell"
      />
    </div>
    <div class="scriptcell-tools">
      <div class="celltype">
        <p>{{ scriptCell.cellType }}</p>
      </div>
      <div class="divider" />
      <div class="icon">
        <img
          src="@/assets/icons/icon-trash.svg"
          alt="trash icon"
          @click="deleteScriptCell(scriptCell.uuid)"
        >
      </div>
      <div class="divider" />
      <div class="icon">
        <img
          src="@/assets/icons/icon-play.svg"
          alt="play icon"
          @click="playScriptCell()"
        >
      </div>
      <div class="divider" />
      <div class="icon handle">
        <img
          src="@/assets/icons/icon-drag.svg"
          alt="drag icon"
        >
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type ScriptCell, CellType, type Scalars, useDeleteScriptCellMutation, type AudioCell, type AudioFile, type DjangoFileType } from '@/graphql';
import ScriptCellMarkdown from './ScriptCellMarkdown.vue';
import ScriptCellCodemirror from './ScriptCellCodemirror.vue';
import ScriptCellAudio from './ScriptCellAudio.vue';
import { ElMessage } from 'element-plus';
import { computed } from 'vue';

type Maybe<T> = T | undefined | null;

type ScriptCellData = Pick<ScriptCell, 'cellType' | 'cellCode' | 'uuid'> & {
  audioCell?: null | undefined | Pick<AudioCell, 'playback' | 'uuid' | 'volume'> & {
    audioFile: Pick<AudioFile, 'uuid' | 'name'> & {
      file?: Maybe<Pick<DjangoFileType, 'url'>>
    }
  }
}

const props = defineProps<{
    scriptCell: ScriptCellData
}>();

const emit = defineEmits<{
  (e: 'update:scriptCell', scriptCell: ScriptCellData): void
}>();


const scriptCellText = computed<string>({
  get() {
    return props.scriptCell.cellCode
  },
  set(value) {
    const newCell = {...props.scriptCell}
    newCell.cellCode = value;
    emit('update:scriptCell', newCell);
    return value;
  },
});

// const sriptCellAudioCell = computed<ScriptCellData['audioCell']>({
//   get() {
//     return props.scriptCell.audioCell ?? undefined;
//   },
//   set(value) {
//     const newCell = {...props.scriptCell};
//     newCell.audioCell = value;
//     emit('update:scriptCell', newCell);
//     return value;
//   }
// });

const displayError = async(message: string) => {
  ElMessage({
      message: message,
      type: "error",
      customClass: "messages-editor",
    });
}

const deleteScriptCellMutation = useDeleteScriptCellMutation();
const deleteScriptCell = async (uuid: Scalars['UUID']) => {
  const {error} = await deleteScriptCellMutation.executeMutation({
    scriptCellUuid: uuid,
  });
  if(error) {
    displayError(error.message);
  }
}

const playScriptCell = () => {
  displayError("Script cell playback not yet implemented");
};

</script>
