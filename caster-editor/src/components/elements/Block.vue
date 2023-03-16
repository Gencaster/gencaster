<template>
  <div>
    <div
      v-if="
        props.cellType === CellType.Comment ||
          props.cellType === CellType.Markdown
      "
    >
      <BlockMarkdown
        :script-cell-uuid="props.scriptCellUuid"
        :index="props.index"
        :dragging="dragging"
      />
    </div>
    <div
      v-if="
        props.cellType === CellType.Python ||
          props.cellType === CellType.Supercollider
      "
    >
      <BlockCodemirror
        :script-cell-uuid="props.scriptCellUuid"
        :index="index"
        :dragging="dragging"
      />
    </div>
    <div
      v-if="
        props.cellType === CellType.Audio
      "
    >
      <BlockAudio
        :script-cell-uuid="props.scriptCellUuid"
        :index="index"
        :dragging="dragging"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
export interface BlockProps {
  scriptCellUuid: String;
  cellType: CellType;
  index: number;
  dragging: boolean;
}

import { CellType } from "@/graphql";
import BlockMarkdown from "./BlockMarkdown.vue";
import BlockCodemirror from "./BlockCodemirror.vue";
import BlockAudio from "./BlockAudio.vue";


const props = defineProps<BlockProps>();
</script>
