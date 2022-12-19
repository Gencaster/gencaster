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
import Header from "@editorjs/header"; // TODO: Fix Could not find a declaration file for module '@editorjs/header'.
import { CellType } from "@/graphql/graphql";
import type { ScriptCell } from "@/graphql/graphql";
import { useGraphStore } from "@/stores/GraphStore";

const props = defineProps<BlockProps>();

interface BlockProps {
  cellData: ScriptCell
  nodeUuid: string
  index: number
}

// Store
const graphStore = useGraphStore();

// Variables
const editorType = ref<string>(props.cellData.cellType);
const editorJS = ref<EditorJS>();
const editorDom = ref<HTMLElement>();
const initData = ref();

// methods
const editorReady = () => {
  console.log("editor ready");
};

const editorChange = (api?: any, event?: any) => {
  editorJS.value?.save().then((outputData) => {
    const newCode = JSON.stringify(outputData);
    graphStore.updateNodeScriptCellLocal(props.nodeUuid, newCode, props.cellData.cellOrder, props.cellData.cellType, props.cellData.uuid);
  }).catch((error) => {
    console.log("Saving failed: ", error);
  });
};

const setUpMarkdown = () => {
  editorJS.value = new EditorJS({
    holder: editorDom.value,
    minHeight: 0,
    tools: {
      header: Header
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
      header: Header
    },
    data: initData.value,
    onReady: editorReady,
    onChange: editorChange
  });
};

onMounted(() => {
  try {
    initData.value = JSON.parse(props.cellData.cellCode);
  }
  catch (error) {
    console.log(error);
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
