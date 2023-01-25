<template>
  <div v-if="props.cellType === CellType.Comment || props.cellType === CellType.Markdown ">
    <ElementsBlockMarkdown
      :script-cell-uuid="props.scriptCellUuid"
      :index="props.index"
      :dragging="dragging"
    />
  </div>
  <div v-if="props.cellType === CellType.Python || props.cellType === CellType.Supercollider ">
    <ElementsBlockCodemirror
      :script-cell-uuid="props.scriptCellUuid"
      :index="index"
      :dragging="dragging"
    />
  </div>
</template>

<script lang="ts" setup>
import { CellType } from "@/graphql/graphql";
const props = defineProps<BlockProps>();

interface BlockProps {
  scriptCellUuid: String
  cellType: CellType
  index: number
  dragging: boolean
}
</script>
