<template>
  <div class="block">
    <!-- markdown -->
    <div v-if="scriptCell?.cellType === CellType.Markdown" class="editor-markdown">
      <div id="editor" ref="editorDom" />
    </div>

    <!-- comment -->
    <div v-if="scriptCell?.cellType === CellType.Comment" class="editor-comment">
      <div ref="editorDom" />
    </div>
  </div>
</template>

<script lang="ts" setup>
// Docs : https://github.com/nhn/tui.editor/tree/master/docs/en
// Custom Markdown Commands: https://github.com/nhn/tui.editor/blob/master/docs/en/plugin.md
import "@toast-ui/editor/dist/toastui-editor.css"; // Editor's Style
import Editor from "@toast-ui/editor";
import type { EditorOptions, Editor as EditorType } from "@toast-ui/editor";

import { storeToRefs } from "pinia";

import { CellType } from "@/graphql/graphql";
import type { GetNodeQuery } from "@/graphql/graphql";
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
const editorDom = ref<HTMLElement>();

// const editorChange = (api?: any, event?: any) => {
//   scriptCellsModified.value = true;
//   editorJS.value?.save().then((outputData) => {
//     console.log(outputData);

//     if (scriptCell.value !== undefined)
//       scriptCell.value.cellCode = outputData.blocks.map((x) => { return x.data.text as string; }).join("\n");
//   });
// };
const editor = ref<EditorType>();

onMounted(() => {
  const options: EditorOptions = {
    el: editorDom.value as HTMLElement,
    height: "auto",
    initialEditType: "markdown",
    usageStatistics: false,
    initialValue: scriptCell.value?.cellCode,
    previewStyle: "tab",
    placeholder: "Please enter text.",
    toolbarItems: [],
    hideModeSwitch: true,
    autofocus: false

  };

  editor.value = new Editor(options);
});
</script>
