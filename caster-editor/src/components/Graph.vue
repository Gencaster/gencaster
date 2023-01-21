<template>
  <div class="index-page">
    <!-- Menu -->
    <div>
      <div class="menu menu-edit">
        <div class="level level-1">
          <div class="menu-items left">
            <el-radio-group v-model="menuStore.tab">
              <el-radio-button :label="Tab.Edit">
                Build
              </el-radio-button>
              <el-radio-button :label="Tab.Test">
                Test
              </el-radio-button>
            </el-radio-group>
          </div>
          <div class="menu-items middle">
            <span>
              {{ graphInStore?.graph.name }}
            </span>
          </div>
          <div class="menu-items right">
            <button class="unstyled state" @click="saveState()">
              <!-- @todo -->
              <div class="state-indicator" :class="{ saved: !true }" />
              Save
            </button>

            <button class="unstyled" @click="exitWithoutSaving()">
              Exit
            </button>
          </div>
        </div>
        <div class="level level-2">
          <div v-if="menuStore.tab === Tab.Edit" class="left">
            <button class="unstyled" @click="addNode()">
              Add Node
            </button>
            <button class="unstyled" :class="{ lighter: hideConnectionButton }" @click="createEdge()">
              Add Connection
            </button>
            <button class="unstyled" :class="{ lighter: hideRemoveButton }" @click="removeAny()">
              Remove
            </button>
            <button class="unstyled" @click="graphStore.reloadFromServer()">
              Refresh
            </button>
          </div>
          <div v-if="menuStore.tab === Tab.Test" />
        </div>
      </div>
      <div class="menu-spacer" />
    </div>

    <!-- Graph -->
    <v-network-graph
      ref="graph"
      v-model:selected-nodes="selectedNodes"
      v-model:selected-edges="selectedEdges"
      class="graph"
      :nodes="graphStore.nodes()"
      :edges="graphStore.edges()"
      :configs="configs"
      :layouts="graphStore.layouts()"
      :event-handlers="eventHandlers"
    />

    <!-- Node Content -->
    <div v-if="showEditor" class="node-data">
      <!-- @todo this can be nil? -->
      <ElementsNodeEditor
        :node-uuid="selectedNodes[0]"
      />
    </div>

    <div v-if="!showEditor" class="stats">
      <p>
        Nodes: {{ graphInStore?.graph.nodes.length }} &nbsp;
        Edges: {{ graphInStore?.graph.edges.length }}
      </p>
    </div>

    <!-- Dialogs -->
    <!-- Are you sure to delete? -->
    <el-dialog v-model="deleteDialogVisible" title="Careful" width="25%" center lock-scroll :show-close="false">
      <span>
        Are you sure to delete Scene "{{ (graph?.nodes[selectedNodes[0]] || { name: "deleted" }).name }}"?
      </span>
      <template #footer>
        <span class="dialog-footer">
          <el-button text bg @click="deleteDialogVisible = false">Cancel</el-button>
          <el-button color="#FF0000" @click="deleteSelectedNodes()">
            Delete Node
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Exit Page -->
    <el-dialog v-model="exitDialogVisible" title="Careful" width="25%" center lock-scroll :show-close="false">
      <span>
        Are you sure to exit without saving? <br> Some of your changes might get lost.
      </span>
      <template #footer>
        <span class="dialog-footer">
          <el-button text bg @click="exitDialogVisible = false">Cancel</el-button>
          <el-button color="#FF0000" @click="exitWithoutSaving()">
            Exit
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ElMessage } from "element-plus";
import type { EventHandlers as GraphEventHandlers, Instance as GraphInstance, Node as GraphNode } from "v-network-graph";
import type { Ref } from "vue";
import { storeToRefs } from "pinia";
import { computed } from "vue";
import { useNodeStore } from "../stores/NodeStore";
import { GraphSettings } from "@/assets/js/graphSettings";
import type { Scalars, ScriptCell } from "@/graphql/graphql";
import { Tab, useMenuStore } from "@/stores/MenuStore";
import { useGraphStore } from "@/stores/GraphStore";
import { useInterfaceStore } from "@/stores/InterfaceStore";
// Props
const props = defineProps<GraphProps>();

// Composables
const router = useRouter();

// Store
const menuStore = useMenuStore();
const graphStore = useGraphStore();
const nodeStore = useNodeStore();
const { graph: graphInStore } = storeToRefs(graphStore);
const { scriptCellsModified, uuid: nodeUuid } = storeToRefs(nodeStore);
const { showEditor } = storeToRefs(useInterfaceStore());

interface GraphProps {
  uuid: Scalars["UUID"]
}

// Data
const graph = ref<GraphInstance>();
const selectedNodeScriptCells: Ref<ScriptCell[]> = ref([]);
const selectedNodes: Ref<string[]> = ref([]);
const selectedEdges: Ref<string[]> = ref([]);

// Config
const configs = GraphSettings.standard;

// Interface
const deleteDialogVisible = ref(false);
const exitDialogVisible = ref(false);
const nodeToDeleteName = ref("");

// Computed
const hideConnectionButton = computed(() => {
  return selectedNodes.value.length !== 2;
});

const curSelectedNode = computed(() => {
  return graphInStore.value?.graph?.nodes.find(x => x.uuid === selectedNodes.value[0]);
});

const hideRemoveButton = computed(() => {
  if ((selectedNodes.value.length === 0 && selectedEdges.value.length === 0) || (selectedNodes.value.length === 0 && selectedEdges.value.length === 0))
    return true;
  else if ((selectedNodes.value.length > 1 || selectedEdges.value.length > 1))
    return true;
  else return false;
});

const addNode = async () => {
  await graphStore.addNode({
    graphUuid: props.uuid,
    name: "new node",
    color: "primary",
    positionX: graph.value?.getPan().x,
    positionY: graph.value?.getPan().y
  });
};

const deleteSelectedNodes = async () => {
  deleteDialogVisible.value = false;
  // work on a copy to not get into problems
  for (const nodeUuid of [...selectedNodes.value])
    await graphStore.deleteNode(nodeUuid);
};

const deleteSelectedEdges = async () => {
  for (const edgeUuid of selectedEdges.value)
    await graphStore.deleteEdge(edgeUuid);
};

const createEdge = async () => {
  if (selectedNodes.value.length !== 2) {
    ElMessage({
      message: "requires exactly 2 scenes selected.",
      type: "error",
      customClass: "messages-editor"
    });
    return;
  }
  const [source, target] = selectedNodes.value;

  await graphStore.createEdge(source, target);
};

const exitWithoutSaving = () => {
  router.push({
    path: "/graphs"
  });
};

const removeAny = () => {
  // check if only one type is selected
  // right now we only allow one element deletion
  // TODO: needs to check if the async call is not buggy if looping through
  if ((selectedNodes.value.length === 1 && selectedEdges.value.length === 0)) {
    deleteDialogVisible.value = true;
  }
  else if ((selectedNodes.value.length === 0 && selectedEdges.value.length === 1)) {
    deleteSelectedEdges();
  }
  else {
    ElMessage({
      message: "Please select max one scene or one connection.",
      type: "error",
      customClass: "messages-editor"
    });
  }
};

const openNodeEditor = async (node: string) => {
  if (scriptCellsModified.value === true) {
    ElMessage({
      message: "Save or close node before opening a new one",
      type: "error",
      customClass: "messages-editor"
    });
    return;
  }
  showEditor.value = true;
  nodeUuid.value = selectedNodes.value[0];
};

const eventHandlers: GraphEventHandlers = {
  // see https://dash14.github.io/v-network-graph/reference/events.html#events-with-event-handlers
  "node:dblclick": ({ node }) => {
    openNodeEditor(node);
  },
  "node:dragend": (dragEvent: { [id: string]: { x: number; y: number } }) => {
    for (const p in dragEvent) {
      const draggedNode = graphInStore.value?.graph.nodes.find(x => x.uuid === p);
      if (draggedNode === undefined) {
        console.log("Could not find dragged Node in our local store");
        continue;
      }
      draggedNode.positionX = dragEvent[p].x;
      draggedNode.positionY = dragEvent[p].y;
      graphStore.updateNodePosition(draggedNode);
    }
  }
};
</script>
