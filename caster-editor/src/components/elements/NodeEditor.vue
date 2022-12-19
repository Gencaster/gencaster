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
      <button @click="addScriptcell(CellType.Markdown, -1)">
        + Markdown
      </button>
      <button @click="addScriptcell(CellType.Python, -1)">
        + Python
      </button>
      <button @click="addScriptcell(CellType.Supercollider, -1)">
        + Supercollider
      </button>
      <button @click="addScriptcell(CellType.Comment, -1)">
        + Comment
      </button>
    </div>
    <div class="blocks">
      <div v-for="(cell, index) in scriptCells" :key="cell.uuid">
        <div class="cell" :class="{ 'no-padding': addNoPaddingClass(cell.cellType) }">
          <div>Icon:<img src="~/assets/icon-trash.jpg" alt=""></div>
          <p class="cell-type">
            {{ index }} -
            {{ cell.uuid }}
          </p>
          <ElementsBlock :ref="el => cells.push(el)" :cell-data="cell" :node-uuid="nodeUuid" :index="index" class="cell-editor" />
          <!-- <div class="scriptcell-tools">
            <p>{{ cell.cellType }}</p>
            <div class="divider" />
            <div><img src="~/assets/icons/icon-down.svg" alt=""></div>
            <div class="divider" />
            <div><img src="~/assets/icons/icon-down.svg" alt=""></div>
            <div class="divider" />
            <div><img src="~/assets/icons/icon-down.svg" alt=""></div>
            <div class="divider" />
            <div><img src="~/assets/icons/icon-down.svg" alt=""></div>
          </div> -->
        </div>
      </div>
    </div>
    <div class="footer">
      <button class="unstyled" @click="toggleShowJSONData()">
        JSON
      </button>
    </div>
    <div v-if="showJSONData" class="json">
      <p>
        <br>
        This is the graphUserState as in the local storage. Not all cell mutations might be commited yet. Save to see latest data.
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
import { json } from "@codemirror/lang-json";
import { computed, ref } from "vue";
import type { Node as GraphNode } from "v-network-graph";

// import type { Node } from "@/graphql/graphql";
// import ElementsBlock from "@/components/elements/ElementsBlock.vue";

import type { ScriptCell, ScriptCellInput } from "@/graphql/graphql";
import { CellType, useCreateScriptCellMutation, useUpdateScriptCellsMutation } from "@/graphql/graphql";
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
const graphStore = useGraphStore();

// Variables
const extensions = [json()];
const cells = ref([]); // TODO: add <typeof ElementsBlock> or what is needed (<InstanceType?) to fix error above

// mutations
const { executeMutation: updateScriptCellsMutation } = useUpdateScriptCellsMutation();
const { executeMutation: createScriptCellMutation } = useCreateScriptCellMutation();

// interface
const showJSONData = ref(false);

// Computed
const graphNodeData: GraphNode = computed(() => {
  return graphStore.graphUserState.nodes[props.nodeUuid];
});

console.log(graphNodeData.value);

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

const addScriptcell = (type: CellType, position: number) => {
  const positionEnd = scriptCells.value.length;

  const variables = {
    nodeUuid: props.nodeUuid,
    order: positionEnd,
    cellType: type
  };

  createScriptCellMutation(variables).then(() => {
    console.log("Added Scriptcell");

    if (position !== -1) {
      console.log("todo: order new cell to certain position"); // TODO: Reorder Cells
    }
    else {
      // TODO: need to refresh cells and before mutate all changes otherwise it will get lost
      console.log("refresh only cells from that node");
      $bus.$emit("refreshAll");
    }
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
