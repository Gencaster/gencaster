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
    <ScriptCellAudio
      v-if="scriptCell.audioCell !== undefined && scriptCell.audioCell !== null && scriptCell.cellType === CellType.Audio"
      v-model:text="scriptCellText"
      v-model:audio-cell="sriptCellAudioCell"
    />

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
import { type ScriptCell, CellType, type Scalars, useDeleteScriptCellMutation, type AudioCell } from '@/graphql';
import ScriptCellMarkdown from './ScriptCellMarkdown.vue';
import ScriptCellCodemirror from './ScriptCellCodemirror.vue';
import ScriptCellAudio from './ScriptCellAudio.vue';
import { ElMessage } from 'element-plus';
import { computed } from 'vue';

export type ScriptCellData = Pick<ScriptCell, 'audioCell' | 'cellType' | 'cellCode' | 'uuid'>

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
  }
});

const sriptCellAudioCell = computed<AudioCell>({
  get() {
    return props.scriptCell.audioCell;
  },
  set(value) {
    const newCell = {...props.scriptCell};
    newCell.audioCell = value;
    emit('update:scriptCell', newCell);
    return value;
  }
});

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
    scriptCellUuid: uuid
  });
  if(error) {
    displayError(error.message);
  }
}

const playScriptCell = () => {
  displayError("Script cell playback not yet implemented");
};

</script>
