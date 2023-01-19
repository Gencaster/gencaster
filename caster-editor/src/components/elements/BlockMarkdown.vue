<template>
  <div class="block">
    <!-- markdown -->
    <div v-if="scriptCell?.cellType === CellType.Markdown" class="editor-markdown">
      <p>This is markdown</p>
      <!-- <div ref="editorDom" /> -->
    </div>

    <!-- comment -->
    <div v-if="scriptCell?.cellType === CellType.Comment" class="editor-comment">
      <p>This is a comment</p>
      <!-- <div ref="editorDom" /> -->
    </div>
  </div>
</template>

<script lang="ts" setup>
// import EditorJS from "@editorjs/editorjs";
// import Header from "@editorjs/header"; // TODO: Fix Could not find a declaration file for module '@editorjs/header'.

import { storeToRefs } from "pinia";
// import type { OutputData } from "@editorjs/editorjs";
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
// const editorJS = ref<EditorJS>();
const editorDom = ref<HTMLElement>();

// const editorChange = (api?: any, event?: any) => {
//   scriptCellsModified.value = true;
//   editorJS.value?.save().then((outputData) => {
//     console.log(outputData);

//     if (scriptCell.value !== undefined)
//       scriptCell.value.cellCode = outputData.blocks.map((x) => { return x.data.text as string; }).join("\n");
//   });
// };

onMounted(() => {
  const splitScriptCell = scriptCell.value?.cellCode.split(/\r\n|\r|\n/) || [];

  // const editorJSInitvalue: OutputData = {
  //   time: Date.now(),
  //   blocks: [],
  //   version: "2.26.4"
  // };

  // splitScriptCell.forEach((string) => {
  //   editorJSInitvalue.blocks.push({
  //     id: self.crypto.randomUUID(),
  //     type: "paragraph",
  //     data: {
  //       text: string
  //     }
  //   });
  // });

  // editorJS.value = new EditorJS({
  //   holder: editorDom.value,
  //   minHeight: 0,
  //   data: editorJSInitvalue,
  //   tools: {
  //     header: Header
  //   },
  //   onChange: editorChange
  // });

  // custom setup for types
  // switch (scriptCell.value?.cellCode) {
  //   case CellType.Comment:
  //     break;

  //   case CellType.Markdown:
  //     break;
  //   default:
  //     break;
  // }
});
</script>
