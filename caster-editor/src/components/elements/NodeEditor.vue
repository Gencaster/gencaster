<template>
  <div class="node-editor-outer">
    <div class="title">
      <div class="left">
        <p>{{ node?.name }}</p>
        <button class="unstyled" @click="renameNodeDialogVisible = true">
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
      <button @click="addScriptcell(CellType.Markdown)">
        + Markdown
      </button>
      <button @click="addScriptcell(CellType.Python)">
        + Python
      </button>
      <button @click="addScriptcell(CellType.Supercollider)">
        + Supercollider
      </button>
      <button @click="addScriptcell(CellType.Comment)">
        + Comment
      </button>
    </div>
    <div class="blocks">
      <div v-for="(cell, index) in node?.scriptCells" :key="cell.uuid">
        <div class="cell" :class="{ 'no-padding': addNoPaddingClass(cell.cellType) }">
          <ElementsBlock
            :ref="el => cells.push(el)" :cell-data="cell" :node-uuid="nodeUuid" :index="index"
            class="cell-editor"
          />
          <div class="scriptcell-tools">
            <div class="celltype">
              <p>{{ cell.cellType }}</p>
            </div>
            <div class="divider" />
            <div class="icon">
              <img src="~/assets/icons/icon-trash.svg" alt="trash icon" @click="deleteScriptCell(cell.uuid)">
            </div>
            <div class="divider" />
            <div class="icon">
              <img src="~/assets/icons/icon-play.svg" alt="play icon" @click="playScriptCell(cell.uuid)">
            </div>
            <div class="divider" />
            <div class="icon">
              <img src="~/assets/icons/icon-up.svg" alt="arrow up icon" @click="moveScriptCell(cell.uuid, 'up')">
            </div>
            <div class="divider" />
            <div class="icon">
              <img src="~/assets/icons/icon-down.svg" alt="arrow down icon" @click="moveScriptCell(cell.uuid, 'down')">
            </div>
          </div>
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
        This is the graphUserState as in the local storage. Not all cell mutations might be commited yet. Save to see
        latest data.
      </p>
      <Codemirror
        v-model="JSONViewerData" placeholder="Code goes here..." :autofocus="false" :indent-with-tab="true"
        :tab-size="2" :extensions="extensions" :disabled="true"
      />
    </div>

    <!-- Change name dialog -->
    <el-dialog v-model="renameNodeDialogVisible" width="25%" title="Rename Node" :show-close="false">
      <el-input v-model="renameNodeDialogName" placeholder="Please input" />
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="renameNodeDialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="renameNodeFromDialog()">
            Confirm
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ElMessage } from "element-plus";
import { Codemirror } from "vue-codemirror";
import { json } from "@codemirror/lang-json";
import { computed, ref } from "vue";
import type { Node as GraphNode } from "v-network-graph";

import { storeToRefs } from "pinia";
import type { ScriptCell, ScriptCellInput } from "@/graphql/graphql";
import { CellType, useCreateScriptCellMutation, useDeleteScriptCellMutation, useUpdateScriptCellsMutation } from "@/graphql/graphql";
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
const { graph } = storeToRefs(graphStore);

// Variables
const extensions = [json()];
const cells = ref([]); // TODO: add <typeof ElementsBlock> or what is needed (<InstanceType?) to fix error above
const renameNodeDialogVisible = ref(false);
const renameNodeDialogName = ref("");

// interface
const showJSONData = ref(false);

// Computed
// nodes list needs to be computed, see
// https://stackoverflow.com/questions/71676111/vue-component-doesnt-update-after-state-changes-in-pinia-store#comment130405154_71677026

const nodes = computed(() => {
  console.log("Recalculate nodes");
  return graph.value.nodes;
});

const node = computed(() => {
  console.log("Recalculated node");
  return nodes.value.find(x => x.uuid === props.nodeUuid);
});

const JSONViewerData = computed(() => {
  return JSON.stringify({ graphUserState: node.value }, null, 2);
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

const renameNodeFromDialog = async () => {
  if (node.value?.name !== undefined) {
    node.value.name = renameNodeDialogName.value;
    graphStore.updateNode(node.value);
    renameNodeDialogVisible.value = false;
  }
};

const mutateCells = () => {
  // const variables: UpdateScriptCellsMutationVariables = {
  //   newCells: ref<ScriptCellInput[]>([])
  // };

  const variables = { // TODO: Needs typed version
    newCells: []
  };

  // set data
  node.value?.scriptCells.forEach((cell) => {
    const newCell: ScriptCellInput = {
      cellCode: cell.cellCode,
      cellOrder: cell.cellOrder,
      cellType: cell.cellType,
      uuid: cell.uuid
    };
  });

  updateScriptCellsMutation(variables).then(() => {
    $bus.$emit("refreshAll");
    // console.log("Updated Scriptcells");
  });
};

const addScriptcell = (type: CellType, position: number | undefined = undefined) => {
  if (node.value === undefined) {
    console.log("You can not add a script cell if not selected properly");
    return;
  }
  // first transfer the current state to the server as otherwise
  // we will reload from the server which may delete edits we have
  // not synced to the server yet
  graphStore.createScriptCell({
    nodeUuid: node.value.uuid,
    order: node.value.scriptCells.length // add to bottom
  });
};

const deleteScriptCell = (scriptCellUuid: string) => {
  const variables = {
    scriptCellUuid
  };

  deleteScriptCellMutation(variables).then(() => {
    console.log(`Deleted ScriptCell ${scriptCellUuid}`);
    $bus.$emit("refreshAll");
  });
};

const playScriptCell = (scriptCellUuid: string) => {
  ElMessage({
    message: "Play not working yet. Sorry :)",
    type: "warning",
    customClass: "messages-editor"
  });
};

const moveScriptCell = (scriptCellUuid: string, direction: string) => {
  const selectedScriptCell: any = [];
  const newOrder: any[] = [];

  node.value?.scriptCells.forEach((scriptCell) => {
    if (scriptCell.uuid === scriptCellUuid)
      selectedScriptCell.push(scriptCell);
    else
      newOrder.push(scriptCell);
  });

  if (selectedScriptCell[0] === undefined) {
    ElMessage({
      message: "Something went wrong changing the order",
      type: "warning",
      customClass: "messages-editor"
    });
    return;
  }

  const oldIndex = selectedScriptCell[0].cellOrder;

  let newPosition = 0;

  if (direction === "up") {
    if (oldIndex > 0)
      newPosition = oldIndex - 1;
  }
  else { // going down
    newPosition = oldIndex + 1; // no need to check anything since it will be re indexed
  }

  newOrder.splice(newPosition, 0, selectedScriptCell[0]);

  // recalculate index for all
  newOrder.forEach((scriptCell, index) => {
    scriptCell.cellOrder = index;
  });

  // graphStore.updateNodeScriptCellsOrderLocal(props.nodeUuid, newOrder);
};

// Styling
const addNoPaddingClass = (blockCellType: CellType) => {
  if (blockCellType === CellType.Markdown || blockCellType === CellType.Comment)
    return true;
  else
    return false;
};
</script>
