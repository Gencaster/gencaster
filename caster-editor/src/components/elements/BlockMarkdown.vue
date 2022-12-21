<template>
  <div class="block">
    <!-- markdown -->
    <div v-if="editorType === CellType.Markdown" class="editor-markdown">
      <div ref="editorDom" />
    </div>

    <!-- comment -->
    <div v-if="editorType === CellType.Comment" class="editor-comment">
      <div ref="editorDom" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import EditorJS from "@editorjs/editorjs";
import { v4 as uuidv4 } from "uuid";
import * as _ from "lodash";
import { CellType } from "@/graphql/graphql";
import type { ScriptCell } from "@/graphql/graphql";
import { useGraphStore } from "@/stores/GraphStore";

const props = defineProps<BlockProps>();

interface BlockProps {
  cellData: ScriptCell
  nodeUuid: string
  index: number
}

interface EditorJSBlockData {
  text?: string
  level?: number
}

interface EditorJSBlock {
  id: string
  type: string
  data: EditorJSBlockData
}

interface EditorJSData {
  time: number
  blocks: EditorJSBlock[]
  version: string
}

// Store
const graphStore = useGraphStore();

// Variables
const editorType = ref<string>(props.cellData.cellType);
const editorJS = ref<EditorJS>();
const editorDom = ref<HTMLElement>();
const initData = ref();
const markdown = ref<string>("");

// methods
const editorReady = () => {
  console.log("editor ready");
};

const parseMarkdownToEditorJS = (string: string) => { // TODO: Outsource to a separate file
  const markdownArray = string.replace(/\r\n/g, "\r").replace(/\n/g, "\r").split(/\r/);

  const data: EditorJSData = {
    version: "2.26.0",
    time: Date.now(),
    blocks: []
  } as EditorJSData;

  markdownArray.forEach((line) => {
    data.blocks.push({
      id: uuidv4(),
      type: "paragraph",
      data: {
        text: line
      }
    });
  });

  return data;
};

const parseEditorJSToMarkdown = (data: EditorJSData) => {
  let markdown = "";

  data.blocks.forEach((block) => {
    switch (block.type) {
      case "paragraph":
        if (block.data.text !== "")
          markdown = `${markdown + block.data.text}\n`;
        break;

      default:
        break;
    }
  });

  // trim trailing new lines
  markdown = _.trim(markdown);

  return markdown;
};

const editorChange = (api?: any, event?: any) => {
  editorJS.value?.save().then((outputData) => {
    // const newCode = JSON.stringify(outputData);

    // revert to markdown
    const newMarkdown = parseEditorJSToMarkdown(outputData as EditorJSData);

    // mutate store local
    // careful: props.index not necessarily the same as cellData.cellOrder
    graphStore.updateNodeScriptCellLocal(props.nodeUuid, newMarkdown, props.index, props.cellData.cellType, props.cellData.uuid);
  }).catch((error) => {
    console.log("Saving failed: ", error);
  });
};

const setUpMarkdown = () => {
  editorJS.value = new EditorJS({
    holder: editorDom.value,
    minHeight: 0,
    tools: {
      // header: Header
    },
    data: initData.value,
    onReady: editorReady,
    onChange: editorChange
  });
};

const setUpComment = () => {
  editorJS.value = new EditorJS({
    holder: editorDom.value,
    minHeight: 0,
    tools: {
      // header: Header
    },
    data: initData.value,
    onReady: editorReady,
    onChange: editorChange
  });
};

onMounted(() => {
  try {
    // initData.value = JSON.parse(props.cellData.cellCode);
    initData.value = parseMarkdownToEditorJS(props.cellData.cellCode);
  }
  catch (error) {
    // console.log(error);
    initData.value = {};
  }

  switch (editorType.value) {
    case CellType.Comment:
      setUpComment();
      break;

    case CellType.Markdown:
      setUpMarkdown();
      break;
    default:
      break;
  }
});

onBeforeUnmount(() => {
  if (editorJS.value)
    editorJS.value.destroy();
});
</script>
