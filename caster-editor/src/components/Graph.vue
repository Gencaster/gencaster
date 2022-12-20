<template>
  <div class="index-page">
    <!-- Menu -->
    <div>
      <div class="menu menu-edit">
        <div class="level level-1">
          <div class="menu-items left">
            <el-radio-group v-model="menuStore.tab">
              <el-radio-button label="edit">
                Build
              </el-radio-button>
              <el-radio-button label="test">
                Test
              </el-radio-button>
              <!-- <el-radio-button label="dev">
                Dev
              </el-radio-button> -->
            </el-radio-group>
          </div>
          <div class="menu-items middle">
            <span>
              {{ graph.name }}
            </span>
          </div>
          <div class="menu-items right">
            <button class="unstyled state" @click="saveState()">
              <div class="state-indicator" :class="{ saved: !graphStore.graphMapDiffers }" />
              Save
            </button>

            <button class="unstyled" @click="exitEditing()">
              Exit
            </button>
          </div>
        </div>
        <div class="level level-2">
          <div v-if="menuStore.tab === 'edit'" class="left">
            <button class="unstyled" @click="addNode()">
              Add Node
            </button>
            <button class="unstyled" :class="{ lighter: hideConnectionButton }" @click="addEdge()">
              Add Connection
            </button>
            <button class="unstyled" :class="{ lighter: hideRemoveButton }" @click="removeAny()">
              Remove
            </button>
            <button class="unstyled" @click="refresh('all')">
              Refresh
            </button>
          </div>
          <div v-if="menuStore.tab === 'test'" />
        </div>
      </div>
      <div class="menu-spacer" />
    </div>

    <!-- Graph -->
    <v-network-graph
      v-model:selected-nodes="selectedNodes" v-model:selected-edges="selectedEdges" class="graph"
      :nodes="graphStore.graphUserState.nodes" :edges="graphStore.graphUserState.edges" :configs="configs"
      :layouts="graphStore.graphUserState.layouts" :event-handlers="eventHandlers"
    />

    <!-- Node Content -->
    <div v-if="interfaceStore.showNodePanel" class="node-data">
      <ElementsNodeEditor :node-uuid="currentNodeUUID" />
    </div>

    <div v-if="!interfaceStore.showNodePanel" class="stats">
      <p>
        Nodes: {{ graph.nodes.length }} &nbsp;
        Edges: {{ graph.edges.length }}
      </p>
    </div>

    <!-- Dialogs -->
    <!-- Are you sure to delete? -->
    <el-dialog v-model="deleteDialogVisible" title="Careful" width="25%" center lock-scroll :show-close="false">
      <span>
        Are you sure to delete Scene "{{ nodeToDeleteName }}"?
      </span>
      <template #footer>
        <span class="dialog-footer">
          <el-button text bg @click="deleteDialogVisible = false">Cancel</el-button>
          <el-button color="#FF0000" @click="removeNode()">
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

<script lang="ts" setup>
import { ElMessage } from "element-plus";
import type { Node as GraphNode } from "v-network-graph";
import type { Ref } from "vue";
import { computed } from "vue";
import { transformEdges, transformLayout, transformNodes } from "@/tools/typeTransformers";
import { GraphSettings } from "@/assets/js/graphSettings";
import type { Graph, Scalars, ScriptCell } from "@/graphql/graphql";
import {
  useCreateEdgeMutation,
  useCreateNodeMutation,
  useDeleteEdgeMutation,
  useDeleteNodeMutation,
  useUpdateNodeMutation
} from "@/graphql/graphql";
import { useMenuStore } from "@/stores/MenuStore";
import { useGraphStore } from "@/stores/GraphStore";
import { useInterfaceStore } from "@/stores/InterfaceStore";
// Props
const props = defineProps<GraphProps>();

const { $bus } = useNuxtApp();

// Composables
const router = useRouter();

// Store
const menuStore = useMenuStore();
const graphStore = useGraphStore();
const interfaceStore = useInterfaceStore();

interface GraphProps {
  graph: Graph
  uuid: Scalars["UUID"]
  fetching: boolean
}

// Data
const currentNodeName = ref<string>("");
const currentNodeUUID = ref<string>("");
const selectedNodeScriptCells: Ref<ScriptCell[]> = ref([]);
const selectedNodes = ref<String[]>([]);
const selectedEdges = ref<String[]>([]);
const nodeInPanel = ref<GraphNode>();

// Config
const configs = GraphSettings.standard;

// Interface
const deleteDialogVisible = ref(false);
const exitDialogVisible = ref(false);
const renameNodeDialogVisible = ref(false);
const renameNodeDialogName = ref("");
const nodeToDeleteName = ref("");

// mutations
// create node
const { executeMutation: createNodeMutation } = useCreateNodeMutation();
// update node
const { executeMutation: updateNodeMutation } = useUpdateNodeMutation();
// remove node
const { executeMutation: removeNodeMutation } = useDeleteNodeMutation();
// create edge
const { executeMutation: createEdgeMutation } = useCreateEdgeMutation();
// remove edge
const { executeMutation: removeEdgeMutation } = useDeleteEdgeMutation();

// Computed
const hideConnectionButton = computed(() => {
  if (selectedNodes.value.length !== 2)
    return true;
  else return false;
});

const hideRemoveButton = computed(() => {
  if ((selectedNodes.value.length === 0 && selectedEdges.value.length === 0) || (selectedNodes.value.length === 0 && selectedEdges.value.length === 0))
    return true;
  else if ((selectedNodes.value.length > 1 || selectedEdges.value.length > 1))
    return true;
  else return false;
});

// Methods
const transformData = (updateLocalState: boolean, updateServerState: boolean) => {
  // push to store
  if (updateLocalState) {
    const nodesLocal = transformNodes(props.graph.nodes);
    const edgesLocal = transformEdges(props.graph.edges);
    const layoutsLocal = transformLayout(props.graph.nodes);
    graphStore.updateGraphLocal(nodesLocal, edgesLocal, layoutsLocal);
  }

  if (updateServerState) {
    // TODO: Is this a good way? Ask Manu
    const nodesServer = JSON.parse(JSON.stringify(transformNodes(props.graph.nodes)));
    const edgesServer = JSON.parse(JSON.stringify(transformEdges(props.graph.edges)));
    const layoutsServer = JSON.parse(JSON.stringify(transformLayout(props.graph.nodes)));
    graphStore.updateGraphServer(nodesServer, edgesServer, layoutsServer);
  }

  console.log("transformed data");
};

const getNodeToDeleteName = () => {
  const uuid = selectedNodes.value[0] as string;
  const node = graphStore.graphUserState.nodes[uuid];
  nodeToDeleteName.value = node.name as string;
};

const emptySelection = () => {
  selectedEdges.value = [];
  selectedNodes.value = [];
};

const refresh = (command: string) => {
  switch (command) {
    case "all":
      if (graphStore.executeQuery !== undefined) {
        graphStore?.executeQuery().then(() => {
          transformData(true, true);
          console.log("finished 'all' refresh");
        });
      }
      break;

    default:
      break;
  }
};

const addNode = () => {
  const variables = {
    graphUuid: props.uuid,
    name: graphStore.defaultNewNodeName,
    color: graphStore.defaultNewNodeColor,
    positionX: 0,
    positionY: 0
  };

  createNodeMutation(variables).then(() => {
    refresh("all");
    console.log("Added node");
  });
};
const removeNode = () => {
  deleteDialogVisible.value = false;
  for (const nodeId of selectedNodes.value) {
    const variables = {
      nodeUuid: nodeId
    };

    removeNodeMutation(variables).then(() => {
      refresh("all");
      console.log("Removed node");
    });
  }
};

const removeEdge = () => {
  for (const edgeId of selectedEdges.value) {
    const variables = {
      edgeUuid: edgeId
    };

    removeEdgeMutation(variables).then(() => {
      refresh("all");
      console.log("Removed edge");
    });
  }
};

const addEdge = () => {
  if (selectedNodes.value.length !== 2) {
    ElMessage({
      message: "requires exactly 2 scenes selected.",
      type: "error",
      customClass: "messages-editor"
    });
    return;
  }
  const [source, target] = selectedNodes.value;

  const variables = {
    nodeInUuid: source,
    nodeOutUuid: target
  };

  createEdgeMutation(variables).then(() => {
    refresh("all");
    console.log("Added edge");
  });
};

const exitEditing = () => {
  if (graphStore.graphMapDiffers) {
    exitDialogVisible.value = true;
  }
  else {
    router.push({
      path: "/graphs"
    });
  }
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
    getNodeToDeleteName();
    // removeNode();
  }
  else if ((selectedNodes.value.length === 0 && selectedEdges.value.length === 1)) {
    removeEdge();
  }
  else {
    ElMessage({
      message: "Please select max one scene or one connection.",
      type: "error",
      customClass: "messages-editor"
    });
  }
};

const updateNode = (uuid: string, name: string | undefined, color: string, positionX: number, positionY: number) => {
  const variables = {
    nodeUuid: uuid,
    name,
    color,
    positionX,
    positionY
  };
  updateNodeMutation(variables).then(() => {
    refresh("all");
    console.log("Updated node");
  });
};

const saveState = () => {
  // update positions
  for (const uuid in graphStore.graphUserState.nodes) { // TODO: This could let to errors if interface is usable while the loops go through
    // get positions
    const n = graphStore.graphUserState.nodes[uuid];
    updateNode(uuid, n.name, n.color, graphStore.graphUserState.layouts.nodes[uuid].x, graphStore.graphUserState.layouts.nodes[uuid].y);
  }
};

const setupNodeDataWindow = (node: string) => {
  currentNodeName.value = graphStore.graphUserState.nodes[node].name as string;
  currentNodeUUID.value = node;
  selectedNodeScriptCells.value = graphStore.graphUserState.nodes[node].scriptCells;
  nodeInPanel.value = graphStore.graphUserState.nodes[node];
};

const doubleClickedNode = (node: string) => {
  if (!interfaceStore.showNodePanel) {
    setupNodeDataWindow(node);
    interfaceStore.showNodePanel = true;
  }
  else {
    ElMessage({
      message: "Close scene data first",
      type: "error",
      customClass: "messages-editor"
    });
  }
};

const nodeDraggedEnd = (node: string) => {
  // const uuid = Object.entries(node);
};

const openNodeNameEdit = () => {
  renameNodeDialogName.value = currentNodeName.value as string;
  renameNodeDialogVisible.value = true;
};

const renameNodeFromDialog = () => {
  if (renameNodeDialogName.value === "") {
    ElMessage({
      message: "Node name can't be empty",
      type: "error",
      customClass: "messages-editor"
    });
    return;
  }

  const uuid = currentNodeUUID.value as string;
  const node = graphStore.graphUserState.nodes[uuid];
  currentNodeName.value = renameNodeDialogName.value;
  updateNode(uuid, renameNodeDialogName.value, node.color, graphStore.graphUserState.layouts.nodes[uuid].x, graphStore.graphUserState.layouts.nodes[uuid].y);
  renameNodeDialogVisible.value = false;
};

const eventHandlers = {
  "node:dblclick": ({ node }: GraphNode) => {
    doubleClickedNode(node);
  },
  "node:dragend": ({ node }: GraphNode) => {
    nodeDraggedEnd(node);
  }
};

const compareGraphStates = () => {
  if (JSON.stringify(graphStore.graphUserState) === JSON.stringify(graphStore.graphServerState))
    return false;
  else
    return true;
};

graphStore.$subscribe((mutation, state) => {
  graphStore.graphMapDiffers = compareGraphStates();
  // console.log("mutated data");
  // console.log(graphStore.graphMapDiffers);
  console.log("Mutation:", mutation);
});

// Events
$bus.$on("closeNodeEditor", () => interfaceStore.showNodePanel = false);
$bus.$on("openNodeNameEdit", () => openNodeNameEdit());
$bus.$on("refreshAll", () => refresh("all"));
$bus.$on("compareState", () => compareGraphStates());

// onMounted
onMounted(() => {
  transformData(true, true);
});
</script>
