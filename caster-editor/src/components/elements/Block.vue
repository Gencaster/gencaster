<template>
  <div>
    <div v-if="cellData.cellType === CellType.Comment || cellData.cellType === CellType.Markdown ">
      <ElementsBlockMarkdown :cell-data="cellData" :node-uuid="nodeUuid" :index="index" class="cell-editor" />
    </div>
    <div v-if="cellData.cellType === CellType.Python || cellData.cellType === CellType.Supercollider ">
      <ElementsBlockCodemirror :cell-data="cellData" :node-uuid="nodeUuid" :index="index" class="cell-editor" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { ScriptCell } from "@/graphql/graphql";
import { CellType } from "@/graphql/graphql";

const props = defineProps<BlockProps>();

interface BlockProps {
  cellData: ScriptCell
  nodeUuid: string
  index: number
}
</script>
