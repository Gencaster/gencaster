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
import type { Node as GraphNode } from "v-network-graph";
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
const graphStore: GraphNode = useGraphStore();

// Block Data
const graphNodeData: GraphNode = computed(() => {
  return graphStore.graphUserState.nodes[props.nodeUuid];
});

// Variables
const editorType = ref<string>(props.cellData.cellType);
const editorJS = ref<EditorJS>();
const editorDom = ref<HTMLElement>();
const editorJSdata = ref<Object>();

// methods
const setUpMarkdown = () => {
  try {
    editorJSdata.value = JSON.parse(props.cellData.cellCode);
  }
  catch (error) {
    console.log(error);
    editorJSdata.value = {};
  }

  editorJS.value = new EditorJS({
    holder: editorDom.value,
    minHeight: 0,
    tools: {
      header: Header
    },
    data: editorJSdata.value as any
  });
};

const setUpComment = () => {
  try {
    editorJSdata.value = JSON.parse(props.cellData.cellCode);
  }
  catch (error) {
    console.log(error);
    editorJSdata.value = {};
  }

  editorJS.value = new EditorJS({
    holder: editorDom.value,
    minHeight: 0,
    tools: {
      header: Header
    },
    data: editorJSdata.value as any
  });
};

onMounted(() => {
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
