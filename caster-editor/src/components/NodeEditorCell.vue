<!-- eslint-disable vue/no-mutating-props -->
<template>
  <div class="cell">
    <ScriptCellMarkdown
      v-if="
        scriptCell.cellType === CellType.Markdown ||
          scriptCell.cellType === CellType.Comment
      "
      v-model:text="scriptCellText"
      :cell-type="scriptCell.cellType"
      :uuid="scriptCell.uuid"
    />
    <ScriptCellCodemirror
      v-if="
        scriptCell.cellType === CellType.Python ||
          scriptCell.cellType === CellType.Supercollider
      "
      v-model:text="scriptCellText"
      :cell-type="scriptCell.cellType"
      :uuid="scriptCell.uuid"
    />
    <div v-if="scriptCell.audioCell !== undefined">
      <ScriptCellAudio
        v-if="
          scriptCell.audioCell !== undefined &&
            scriptCell.audioCell !== null &&
            scriptCell.audioCell?.audioFile.file !== undefined &&
            scriptCell.cellType === CellType.Audio
        "
        v-model:text="scriptCellText"
        v-model:audio-cell="scriptCell.audioCell"
        :uuid="scriptCell.uuid"
      />
    </div>
    <div class="scriptcell-tools">
      <div
        class="celltype"
        @click="openHelp(scriptCell.cellType)"
      >
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
import {
  type ScriptCell,
  CellType,
  type Scalars,
  useDeleteScriptCellMutation,
  type AudioCell,
  type AudioFile,
  type DjangoFileType,
} from "@/graphql";
import ScriptCellMarkdown from "./ScriptCellMarkdown.vue";
import ScriptCellCodemirror from "./ScriptCellCodemirror.vue";
import ScriptCellAudio from "./ScriptCellAudio.vue";
import { ElMessage } from "element-plus";
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useInterfaceStore } from "@/stores/InterfaceStore";

type Maybe<T> = T | undefined | null;

type ScriptCellData = Pick<ScriptCell, "cellType" | "cellCode" | "uuid"> & {
  audioCell?:
    | null
    | undefined
    | (Pick<AudioCell, "playback" | "uuid" | "volume"> & {
        audioFile: Pick<AudioFile, "uuid" | "name"> & {
          file?: Maybe<Pick<DjangoFileType, "url">>;
        };
      });
};

const props = defineProps<{
  scriptCell: ScriptCellData;
}>();

const { newScriptCellUpdates } = storeToRefs(useInterfaceStore());

const scriptCellText = computed<string>({
  get() {
    return props.scriptCell.cellCode;
  },
  set(value) {
    const newCell = { ...props.scriptCell };
    newCell.cellCode = value;
    return value;
  },
});

const deleteScriptCellMutation = useDeleteScriptCellMutation();
const deleteScriptCell = async (uuid: Scalars["UUID"]) => {
  if (newScriptCellUpdates.value.size > 0) {
    // deleting a script cell triggers refresh from the server, so in order to not
    // loose any changes it is necessary to save them before
    ElMessage.info(
      "There are unsaved changes. Please save the changes before deleting a script cell",
    );
    return;
  }
  const { error } = await deleteScriptCellMutation.executeMutation({
    scriptCellUuid: uuid,
  });
  if (error) {
    ElMessage.error(`Error on deleting the script cell: ${error.message}`);
  }
};

const playScriptCell = () => {
  ElMessage.error("Script cell playback not yet implemented");
};

const openHelp = (cellType: CellType) => {
  let helpUrl = "https://docs.gencaster.org";
  switch (cellType) {
    case CellType.Audio: {
      helpUrl = `${helpUrl}/editor.html#audio`;
      break;
    }
    case CellType.Comment: {
      helpUrl = `${helpUrl}/editor.html#comment`;
      break;
    }
    case CellType.Markdown: {
      helpUrl = `${helpUrl}/editor.html#markdown`;
      break;
    }
    case CellType.Python: {
      helpUrl = `${helpUrl}/editor.html#python`;
      break;
    }
    case CellType.Supercollider: {
      helpUrl = `${helpUrl}/editor.html#supercollider`;
      break;
    }
  }
  window.open(helpUrl, "_blank");
};
</script>
