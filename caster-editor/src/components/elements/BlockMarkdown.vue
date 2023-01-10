<template>
  <div class="block">
    <!-- markdown -->
    <div
      v-if="scriptCell?.cellType === CellType.Markdown"
      class="editor-markdown"
    >
      <div ref="editorDom" />
    </div>

    <!-- comment -->
    <div
      v-if="scriptCell?.cellType === CellType.Comment"
      class="editor-comment"
    >
      <div ref="editorDom" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import EditorJS from "@editorjs/editorjs";
import Header from "@editorjs/header"; // TODO: Fix Could not find a declaration file for module '@editorjs/header'.
import type { Ref } from "vue";
import { storeToRefs } from "pinia";
import { CellType } from "@/graphql/graphql";
import type { GetNodeQuery, ScriptCell } from "@/graphql/graphql";
import { useNodeStore } from "@/stores/NodeStore";

const props = defineProps<BlockProps>();

interface BlockProps {
  scriptCellUuid: String
  index: number
}

// Store
const { scriptCellsModified, node } = storeToRefs(useNodeStore());

// Variables
const scriptCell = ref<GetNodeQuery["node"]["scriptCells"][0] | undefined>(node.value.scriptCells.find((x) => { return x.uuid === props.scriptCellUuid; }));
const editorJS = ref<EditorJS>();
const editorDom = ref<HTMLElement>();
const initData = ref();

const editorChange = (api?: any, event?: any) => {
  scriptCellsModified.value = true;
  editorJS.value?.save().then((outputData) => {
    if (scriptCell.value !== undefined)
      scriptCell.value.cellCode = outputData.blocks.map((x) => { return x.data.text as string; }).join("\n");
  });
};

onMounted(() => {
  editorJS.value = new EditorJS({
    holder: editorDom.value,
    minHeight: 0,
    tools: {
      header: Header
    },
    // @todo scriptCell.value?.cellCode ??
    onChange: editorChange
  });

  // @todo editorjs does need json but we don't have json in backend
  // initData.value = JSON.parse(scriptCell.value?.cellCode || "{}");

  switch (scriptCell.value?.cellCode) {
    case CellType.Comment:
      break;

    case CellType.Markdown:
      break;
    default:
      break;
  }
});
</script>
