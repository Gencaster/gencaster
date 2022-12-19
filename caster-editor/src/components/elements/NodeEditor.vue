<template>
  <div class="node-editor-outer">
    <div class="title">
      <div class="left">
        <p>{{ currentNodeName }}</p>
        <button class="unstyled" @click="openNodeNameEdit()">
          edit
        </button>
      </div>
      <div class="right">
        <button class="unstyled" @click="mutateCells()">
          Save Scene
        </button>
        <button class="unstyled" @click="closeNodeEditor()">
          Close
        </button>
      </div>
    </div>
    <div class="node-menu-bar">
      <el-button text bg :icon="Plus" />
      <el-button text bg :icon="Scissor" />
      <el-button text bg :icon="VideoPlay" />
      <el-button text bg :icon="VideoPause" />
    </div>
    <div class="blocks">
      <div v-for="(cell, index) in scriptCells" :key="cell.uuid">
        <div class="cell" :class="{ 'no-padding': addNoPaddingClass(cell.cellType) }">
          <p class="cell-type">
            {{ index }} -
            {{ cell.uuid }} -
            {{ cell.cellType }}
          </p>
          <ElementsBlock :ref="el => cells.push(el)" :cell-data="cell" :node-uuid="nodeUuid" :index="index" class="cell-editor" />
        </div>
      </div>
    </div>
    <div class="footer">
      <button class="unstyled" @click="toggleShowJSONData()">
        JSON
      </button>
    </div>
    <div v-if="showJSONData" class="json">
      <p style="font-style: italic;">
        <br>
        This is the graphUserState as in the local storage. Not all cell mutations might be commited yet. Save to see all changes.
      </p>
      <Codemirror
        v-model="JSONViewerData" placeholder="Code goes here..." :autofocus="false" :indent-with-tab="true"
        :tab-size="2" :extensions="extensions" :disabled="true"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Codemirror } from "vue-codemirror";
import { Plus, Scissor, VideoPause, VideoPlay } from "@element-plus/icons-vue";
import { json } from "@codemirror/lang-json";
import { computed, ref } from "vue";

// import type { Node } from "@/graphql/graphql";
import type { Node as GraphNode } from "v-network-graph";
// import ElementsBlock from "@/components/elements/ElementsBlock.vue";

import type { ScriptCell, ScriptCellInput, UpdateScriptCellsMutationVariables } from "@/graphql/graphql";
import { CellType, useUpdateScriptCellsMutation } from "@/graphql/graphql";
import { useGraphStore } from "@/stores/GraphStore";

const props = defineProps({
  dev: {
    type: Boolean,
    default: false
  },
  nodeUuid: {
    required: true,
    type: String
  }
});

// bus
const { $bus } = useNuxtApp();

// Store
const graphStore: GraphNode = useGraphStore();

// Variables
const extensions = [json()];
const cells = ref([]); // TODO: add <typeof ElementsBlock> or what is needed (<InstanceType?)

// mutations
const { executeMutation: updateScriptCellsMutation } = useUpdateScriptCellsMutation();

// interface
const showJSONData = ref(false);

// Computed
const graphNodeData: GraphNode = computed(() => {
  return graphStore.graphUserState.nodes[props.nodeUuid];
});

const scriptCells = computed(() => {
  return graphNodeData.value.scriptCells as ScriptCell[];
});

const currentNodeName = computed(() => {
  return graphNodeData.value.name;
});

const JSONViewerData = computed(() => {
  return JSON.stringify({ graphUserState: scriptCells.value }, null, 2);
});

// Methods
const openNodeNameEdit = () => {
  $bus.$emit("openNodeNameEdit");
};

const closeNodeEditor = () => {
  $bus.$emit("closeNodeEditor");
};

const toggleShowJSONData = () => {
  showJSONData.value = !showJSONData.value;
};

const mutateCells = () => {
  // const variables: UpdateScriptCellsMutationVariables = {
  //   newCells: ref<ScriptCellInput[]>([])
  // };

  const variables = { // TODO: Needs typed version
    newCells: []
  };

  // set data
  scriptCells.value.forEach((cell: ScriptCell) => {
    const newCell: ScriptCellInput = {
      cellCode: cell.cellCode,
      cellOrder: cell.cellOrder,
      cellType: cell.cellType,
      uuid: cell.uuid
    };
    variables.newCells.push(newCell); // TODO: Needs typed version
    console.log(cell.uuid);
  });

  updateScriptCellsMutation(variables).then(() => {
    console.log("Updated Scriptcells");
  });
};

// Styling
const addNoPaddingClass = (blockCellType: CellType) => {
  if (blockCellType === CellType.Markdown || blockCellType === CellType.Comment)
    return true;
  else
    return false;
};
</script>
