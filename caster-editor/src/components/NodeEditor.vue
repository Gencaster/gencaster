<template>
  <div>
    <div v-if="!node || stale" />
    <div v-else>
      <div class="title">
        <div class="left">
          <p>{{ node?.node.name }}</p>
          <button
            class="unstyled"
            @click="openNodeRenameDialog()"
          >
            edit
          </button>
        </div>
        <div class="right">
          <button
            class="unstyled"
            :disabled="!scriptCellsModified"
            @click="syncCellsWithServer()"
          >
            Save Scene
          </button>
          <button
            class="unstyled"
            @click="clickedClose()"
          >
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
        <draggable
          v-if="nodeDataReady"
          v-model="scriptCellList"
          item-key="uuid"
          handle=".handle"
          @start="dragging = true"
          @end="dragging = false"
        >
          <template #item="{ element }">
            <div :class="{ 'no-padding': addNoPaddingClass(element.cellType) }">
              <div
                class="cell"
                :class="{ dragging }"
              >
                <Block
                  :script-cell-uuid="element.uuid"
                  :cell-type="element.cellType"
                  :index="element.cellOrder"
                  :dragging="dragging"
                />
                <div class="scriptcell-tools">
                  <div class="celltype">
                    <p>{{ element.cellType }}</p>
                  </div>
                  <div class="divider" />
                  <div class="icon">
                    <img
                      src="@/assets/icons/icon-trash.svg"
                      alt="trash icon"
                      @click="deleteScriptCell(element.uuid)"
                    >
                  </div>
                  <div class="divider" />
                  <div class="icon">
                    <img
                      src="@/assets/icons/icon-play.svg"
                      alt="play icon"
                      @click="playScriptCell()"
                    >
                  </div>
                  <div class="divider" />
                  <div class="icon handle">
                    <img
                      src="@/assets/icons/icon-drag.svg"
                      alt="drag icon"
                    >
                  </div>
                </div>
              </div>
            </div>
          </template>
        </draggable>
      </div>

      <div
        v-if="nodeDataReady"
        class="footer"
      >
        <button
          class="unstyled"
          @click="
            () => {
              showJSONData = !showJSONData;
            }
          "
        >
          JSON
        </button>
      </div>
      <div
        v-if="showJSONData"
        class="json"
      >
        <p>
          <br>
          This is the graphUserState as in the local storage. Not all cell
          mutations might be committed yet. Save to see latest data.
        </p>
        <Codemirror
          v-model="JSONViewerData"
          placeholder="Code goes here..."
          :autofocus="false"
          :indent-with-tab="true"
          :tab-size="2"
          :extensions="[json()]"
          :disabled="true"
        />
      </div>

      <!-- Close node dialog -->
      <ElDialog
        v-model="closeNodeDialogVisible"
        title="Careful"
        width="25%"
        center
        lock-scroll
        :show-close="false"
      >
        <span>
          Unsaved changes in the editor! <br>
          Are you sure to exit without saving?
        </span>
        <template #footer>
          <span class="dialog-footer">
            <ElButton
              text
              bg
              @click="closeNodeDialogVisible = false"
            >
              Cancel
            </ElButton>
            <ElButton
              text
              bg
              @click="closeWithoutSaving()"
            >
              Close without saving
            </ElButton>
            <ElButton
              color="#ADFF00"
              @click="saveAndClose()"
            >
              Save and Close
            </ElButton>
          </span>
        </template>
      </ElDialog>

      <!-- Change name dialog -->
      <ElDialog
        v-model="renameNodeDialogVisible"
        width="25%"
        title="Rename Node"
        :show-close="false"
      >
        <ElInput
          v-model="renameNodeDialogName"
          placeholder="Please input"
        />
        <template #footer>
          <span class="dialog-footer">
            <ElButton @click="renameNodeDialogVisible = false">Cancel</ElButton>
            <ElButton
              color="#ADFF00"
              type="primary"
              @click="renameNodeFromDialog()"
            >
              Confirm
            </ElButton>
          </span>
        </template>
      </ElDialog>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ElMessage } from "element-plus";
import { Codemirror } from "vue-codemirror";
import { json } from "@codemirror/lang-json";
import type { Ref } from "vue";
import { computed, ref } from "vue";
import { storeToRefs } from "pinia";
import { CellType, type GraphSubscription } from "@/graphql";
import draggable from "vuedraggable";
import Block from "./elements/Block.vue";
import { useNodeStore } from "@/stores/NodeStore";
import { useGraphStore } from "@/stores/GraphStore";
import { useInterfaceStore } from "@/stores/InterfaceStore";

enum MoveDirection {
  up = "Up",
  down = "Down",
}


// Store
const nodeStore = useNodeStore();
const { node, scriptCellsModified, stale, nodeDataReady, uuid: nodeUuid } = storeToRefs(nodeStore);
const { showEditor } = storeToRefs(useInterfaceStore());
const {selectedEdges, selectedNodes} = storeToRefs(useGraphStore());


// Variables
const renameNodeDialogVisible: Ref<boolean> = ref(false);
const renameNodeDialogName: Ref<string> = ref("");
const closeNodeDialogVisible: Ref<boolean> = ref(false);

// Drag
const dragging: Ref<boolean> = ref(false);

// interface
const showJSONData: Ref<boolean> = ref(false);

const JSONViewerData = computed(() => {
  return JSON.stringify({ graphUserState: node.value }, null, 2);
});

const closeEditor = async () => {
  showEditor.value = false;
  selectedEdges.value = [];
  selectedNodes.value = [];
  nodeUuid.value = undefined;
};

const clickedClose = async () => {
  console.log('clicked close without saving')
  if (scriptCellsModified.value) {
    closeNodeDialogVisible.value = true;
    return;
  }
  await closeEditor();
};

const closeWithoutSaving = () => {
  scriptCellsModified.value = false;
  closeNodeDialogVisible.value = false;
  closeEditor();
};

const saveAndClose = async () => {
  closeNodeDialogVisible.value = false;
  await syncCellsWithServer().then(async () => {
    await closeEditor();
    console.log('closed');
  });
}

const renameNodeFromDialog = async () => {
  if (node.value === undefined) {
    console.log("Need a valid node for rename");
    return;
  }
  node.value.node.name = renameNodeDialogName.value;
  await nodeStore.updateNode(node.value.node);
  renameNodeDialogVisible.value = false;
};

const openNodeRenameDialog = () => {
  if (node.value === undefined) {
    console.log("Need a valid node for rename");
    return;
  }
  renameNodeDialogName.value = node.value.node.name;
  renameNodeDialogVisible.value = true;
}


const syncCellsWithServer = async () => {
  if (node.value?.node !== undefined)
    await nodeStore.updateScriptCells(node.value.node.scriptCells);
};

const addScriptCell = (type: CellType) => {
  if (node.value === undefined) {
    console.log("You can not add a script cell if not selected properly");
    return;
  }
  // first transfer the current state to the server as otherwise
  // we will reload from the server which may delete edits we have
  // not synced to the server yet
  nodeStore.createScriptCell({
    nodeUuid: node.value.node.uuid,
    newScriptCell: {
      // add cell as last cell by searching for highest current cell order
      cellOrder:
        node.value.node.scriptCells.length > 0
          ? Math.max(
            ...node.value.node.scriptCells.map((x) => {
              return x.cellOrder;
            })
          ) + 1
          : 0,
      cellCode: "",
      cellType: type,
    },
  });
};

const deleteScriptCell = async (scriptCellUuid: string) => {
  await nodeStore.deleteScriptCell(scriptCellUuid);
};

const playScriptCell = () => {
  ElMessage({
    message: "Play not working yet. Sorry :)",
    type: "warning",
    customClass: "messages-editor",
  });
};

/**
 * Manages the scriptcell array.
 * get() Returns the current one from the store
 * set() Updates it and also resets the orders
 */
const scriptCellList = computed({
  get() {
    if (node.value) return node.value.node?.scriptCells;
    else return [];
  },
  set(value) {
    if (node.value === undefined) {
      console.log("Need a valid node for scriptcells");
      return;
    }

    const newOrder: Array<
      GraphSubscription["graph"]["nodes"][0]["scriptCells"][0]
    > = [];

    value.forEach((scriptCell) => {
      newOrder.push(scriptCell);
    });

    // recalculate index for all
    newOrder.forEach((scriptCell, index) => {
      scriptCell.cellOrder = index;
    });

    // update local store with newOrder
    node.value.node.scriptCells = newOrder;

    // set the state to modified
    scriptCellsModified.value = true;
  },
});


// eslint-disable-next-line @typescript-eslint/no-unused-vars
const moveScriptCell = async (
  scriptCellUuid: string,
  direction: MoveDirection
) => {
  if (node.value === undefined) {
    console.log("Need a valid node for scriptcells");
    return;
  }

  const selectedScriptCell: Array<
    GraphSubscription["graph"]["nodes"][0]["scriptCells"][0]
  > = [];

  const newOrder: Array<
    GraphSubscription["graph"]["nodes"][0]["scriptCells"][0]
  > = [];

  node.value?.node.scriptCells.forEach((scriptCell) => {
    if (scriptCell.uuid === scriptCellUuid) selectedScriptCell.push(scriptCell);
    else newOrder.push(scriptCell);
  });

  if (selectedScriptCell[0] === undefined) {
    ElMessage({
      message: "Something went wrong changing the order",
      type: "warning",
      customClass: "messages-editor",
    });
    return;
  }

  const oldIndex = selectedScriptCell[0].cellOrder;

  // catch if nothing changes
  if (direction === MoveDirection.up && oldIndex === 0) return;

  if (
    direction === MoveDirection.down &&
    oldIndex === node.value?.node.scriptCells.length - 1
  )
    return;

  let newPosition = 0;
  if (direction === MoveDirection.up) {
    if (oldIndex > 0) newPosition = oldIndex - 1;
  } else {
    // going down
    newPosition = oldIndex + 1; // no need to check anything since it will be re indexed
  }

  newOrder.splice(newPosition, 0, selectedScriptCell[0]);

  // recalculate index for all
  newOrder.forEach((scriptCell, index) => {
    scriptCell.cellOrder = index;
  });

  // commit to store
  await nodeStore.updateScriptCells(newOrder);
};

// Styling
const addNoPaddingClass = (blockCellType: CellType) => {
  return (
    blockCellType === CellType.Markdown || blockCellType === CellType.Comment
  );
};

// lets try if it works w/o this?
// onUnmounted(() => {
//   node.value = undefined;
// });
</script>
