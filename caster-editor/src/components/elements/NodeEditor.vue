<template>
  <div v-if="fetching">
    <ElementsLoading />
  </div>
  <div v-else class="node-editor-outer">
    <div class="title">
      <div class="left">
        <p>{{ node.name }}</p>
        <button class="unstyled" @click="renameNodeDialogVisible = true">
          edit
        </button>
      </div>
      <div class="right">
        <button class="unstyled" :disabled="!scriptCellsModified" @click="syncCellsWithServer()">
          Save Scene
        </button>
        <button class="unstyled" @click="clickedClose()">
          Close
        </button>
      </div>
    </div>
    <div class="node-menu-bar">
      <button @click="addScriptCell(CellType.Markdown)">
        + Markdown
      </button>
      <button @click="addScriptCell(CellType.Python)">
        + Python
      </button>
      <button @click="addScriptCell(CellType.Supercollider)">
        + Supercollider
      </button>
      <button @click="addScriptCell(CellType.Comment)">
        + Comment
      </button>
    </div>
    <div class="blocks">
      <div v-for="(cell, index) in node.scriptCells.sort(x => x.cellOrder)" :key="cell.uuid">
        <div class="cell" :class="{ 'no-padding': addNoPaddingClass(cell.cellType) }">
          <ElementsBlock
            :script-cell-uuid="cell.uuid"
            :cell-type="cell.cellType"
            :index="index"
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
              <img src="~/assets/icons/icon-up.svg" alt="arrow up icon" @click="moveScriptCell(cell.uuid, MoveDirection.up)">
            </div>
            <div class="divider" />
            <div class="icon">
              <img src="~/assets/icons/icon-down.svg" alt="arrow down icon" @click="moveScriptCell(cell.uuid, MoveDirection.down)">
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="footer">
      <button class="unstyled" @click="() => { showJSONData = !showJSONData }">
        JSON
      </button>
    </div>
    <div v-if="showJSONData" class="json">
      <p>
        <br>
        This is the graphUserState as in the local storage. Not all cell mutations might be committed yet. Save to see
        latest data.
      </p>
      <Codemirror
        v-model="JSONViewerData" placeholder="Code goes here..." :autofocus="false" :indent-with-tab="true"
        :tab-size="2" :extensions="[json()]" :disabled="true"
      />
    </div>

    <!-- Exit Page -->
    <el-dialog v-model="exitDialogVisible" title="Careful" width="25%" center lock-scroll :show-close="false">
      <span>
        You have unsaved changes! <br>
        Are you sure to exit without saving?
      </span>
      <template #footer>
        <span class="dialog-footer">
          <el-button text bg @click="exitDialogVisible = false">Stop</el-button>
          <el-button
            color="#00ff00" text bg @click="async () => {
              exitDialogVisible = false;
              await syncCellsWithServer().then(async () => {
                await closeEditor();
              });
            }"
          >Save and exit</el-button>
          <el-button color="#FF0000" @click="closeEditor()">Exit without saving</el-button>
        </span>
      </template>
    </el-dialog>

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
import type { Ref } from "vue";
import { computed, ref } from "vue";

import { storeToRefs } from "pinia";
import { useNodeStore } from "@/stores/NodeStore";
import { CellType } from "@/graphql/graphql";
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

enum MoveDirection {
  up = "Up",
  down = "Down"
}

// bus
const { $bus } = useNuxtApp();

// Store
const nodeStore = useNodeStore();
const { node, fetching, scriptCellsModified } = storeToRefs(nodeStore);
const graphStore = useGraphStore();

// Variables
const renameNodeDialogVisible = ref(false);
const renameNodeDialogName = ref("");
const exitDialogVisible: Ref<boolean> = ref(false);

// interface
const showJSONData = ref(false);

const JSONViewerData = computed(() => {
  return JSON.stringify({ graphUserState: node.value }, null, 2);
});

const closeEditor = async () => {
  // Graph view is responsible for removing us
  await $bus.$emit("closeNodeEditor");
};

const clickedClose = async () => {
  if (scriptCellsModified.value) {
    exitDialogVisible.value = true;
    return;
  }
  await closeEditor();
};

const renameNodeFromDialog = async () => {
  if (node.value === undefined) {
    console.log("Need a valid node for rename");
    return;
  }
  node.value.name = renameNodeDialogName.value;
  await nodeStore.updateNode(node.value);
  // updates the name on the graph view as well
  await graphStore.reloadFromServer();
  renameNodeDialogVisible.value = false;
};

const syncCellsWithServer = async () => {
  await nodeStore.updateScriptCells(node.value.scriptCells).then(() => {
    console.log("Updated cells on server successfully");
    scriptCellsModified.value = false;
  });
};

const addScriptCell = (type: CellType, position: number | undefined = undefined) => {
  if (node.value === undefined) {
    console.log("You can not add a script cell if not selected properly");
    return;
  }
  // first transfer the current state to the server as otherwise
  // we will reload from the server which may delete edits we have
  // not synced to the server yet
  nodeStore.createScriptCell({
    nodeUuid: node.value.uuid,
    order: node.value.scriptCells.length // add to bottom
  });
};

const deleteScriptCell = async (scriptCellUuid: string) => {
  await nodeStore.deleteScriptCell(scriptCellUuid);
};

const playScriptCell = (scriptCellUuid: string) => {
  ElMessage({
    message: "Play not working yet. Sorry :)",
    type: "warning",
    customClass: "messages-editor"
  });
};

const moveScriptCell = (scriptCellUuid: string, direction: MoveDirection) => {
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

  if (direction === MoveDirection.up) {
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
  return blockCellType === CellType.Markdown || blockCellType === CellType.Comment;
};

onMounted(() => {
  nodeStore.getNode(props.nodeUuid);
});
</script>
