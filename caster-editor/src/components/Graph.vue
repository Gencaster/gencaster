<template>
  <div class="index-page">
    <!-- Menu -->
    <div>
      <div class="menu menu-edit">
        <div class="level level-1">
          <div class="menu-items left">
            <el-radio-group v-model="menuStore.tab">
              <el-radio-button label="edit">
                Edit
              </el-radio-button>
              <el-radio-button label="test">
                Test
              </el-radio-button>
              <el-radio-button label="dev">
                Dev
              </el-radio-button>
            </el-radio-group>
          </div>
          <div class="menu-items middle">
            <span>
              {{ graph.name }}
            </span>
          </div>
          <div class="menu-items right">
            <button class="unstyled state" @click="saveState()">
              <div class="state-indicator" :class="{ saved: stateSaved }" />
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
            <!-- <button class="unstyled" :disabled="selectedNodes.length !== 2" @click="addEdge()"> -->
            <button class="unstyled" :class="{ lighter: hideConnectionButton }" @click="addEdge()">
              Add Connection
            </button>
            <button class="unstyled" :class="{ lighter: hideRemoveButton }" @click="removeAny()">
              Remove
            </button>
            <button class="unstyled" @click="refresh()">
              Refresh
            </button>
          </div>
          <div v-if="menuStore.tab === 'test'" />
        </div>
      </div>
      <div class="menu-spacer" />
    </div>

    <!-- Graph -->
    <div>
      <v-network-graph
        v-model:selected-nodes="selectedNodes" v-model:selected-edges="selectedEdges" class="graph"
        :nodes="nodes" :edges="edges" :configs="configs" :layouts="layouts" :event-handlers="eventHandlers"
      />

      <p v-if="showGraphData">
        {{ nodes }}
        <br>
        {{ layouts }}
        <br>
        {{ graph }}
        <!-- {{ graphData }} -->
      </p>

      <div v-if="showNodeData" class="node-data">
        <ElementsBlockEditor :current-node-name="currentNodeName" :blocks-data="selectedNodeScriptCells" />
      </div>

      <div v-if="!showNodeData" class="stats">
        <p>
          Nodes: {{ graph.nodes.length }} &nbsp;
          Edges: {{ graph.edges.length }}
        </p>
      </div>

      <!-- Dialogs -->
      <!-- Exit Page -->
      <!-- <el-dialog v-model="exitDialogVisible" title="Careful" width="25%" center lock-scroll :show-close="false">
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
      </el-dialog> -->
      <!-- Change name dialog -->
      <!-- <el-dialog v-model="renameNodeDialogVisible" width="25%" title="Rename Node" :show-close="false">
        <el-input v-model="renameNodeDialogName" placeholder="Please input" />
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="renameNodeDialogVisible = false">Cancel</el-button>
            <el-button type="primary" @click="renameNodeFromDialog()">
              Confirm
            </el-button>
          </span>
        </template>
      </el-dialog> -->
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { Edges, Node, Nodes } from "v-network-graph";
import type { Ref } from "vue";
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { GraphSettings } from "../assets/js/graphSettings";
import {
  useCreateEdgeMutation,
  useCreateNodeMutation,
  useDeleteEdgeMutation,
  useDeleteNodeMutation,
  useGetGraphQuery,
  useUpdateNodeMutation
} from "../graphql/graphql";
import type { Graph, Scalars, ScriptCell } from "../graphql/graphql";
import { transformEdges, transformLayout, transformNodes } from "../tools/typeTransformers";
import { useMenuStore } from "@/stores/MenuStore";
import { useGraphStore } from "@/stores/GraphStore";

// Props
const props = defineProps<GraphProps>();

// Store
const menuStore = useMenuStore();
const graphStore = useGraphStore();

interface GraphProps {
  graph: Graph
  uuid: Scalars["UUID"]
}

// Data
const showGraphData = ref(false);
const showNodeData = ref(false);
const stateSaved = ref(false);
const currentNodeName = ref<string>();
const currentNodeUUID = ref<string>();
const selectedNodeScriptCells: Ref<ScriptCell[]> = ref([]);

const configs = GraphSettings.standard;
const nodes: Ref<Nodes> = ref(transformNodes(props.graph.nodes));
const edges: Ref<Edges> = ref(transformEdges(props.graph.edges));
const layouts: Ref<Nodes> = ref(transformLayout(props.graph.nodes));
const selectedNodes = ref<String[]>([]);
const selectedEdges = ref<String[]>([]);

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
  else
    return false;
});

const hideRemoveButton = computed(() => {
  if ((selectedNodes.value.length === 0 && selectedEdges.value.length === 0) || (selectedNodes.value.length === 0 && selectedEdges.value.length === 0))
    return true;
  else if ((selectedNodes.value.length > 1 || selectedEdges.value.length > 1))
    return true;
  else
    return false;
});

// Methods
const transformData = () => {
  nodes.value = transformNodes(props.graph.nodes);
  edges.value = transformEdges(props.graph.edges);
  layouts.value = transformLayout(props.graph.nodes);
};

const refresh = () => {
  if (graphStore.executeQuery !== undefined) {
    graphStore?.executeQuery().then(() => {
      transformData();
      selectedNodes.value = [];
      selectedEdges.value = [];
      console.log("finished refresh");
    });
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
    refresh();
    console.log("Added node");
  });
};
const addEdge = () => {};
const exitEditing = () => {};

const removeAny = () => {};
const saveState = () => {};
const setupNodeDataWindow = (node: string) => {
  currentNodeName.value = nodes.value[node].name;
  currentNodeUUID.value = node;

  const cells = nodes.value[node].scriptCells;
  selectedNodeScriptCells.value = cells;
};

const doubleClickedNode = (node: string) => {
  setupNodeDataWindow(node);
  showNodeData.value = true;
  console.log("dblclick");
  console.log(nodes.value[node]);
};

const nodeDraggedEnd = (node: string) => {
  // const uuid = Object.entries(node);
};

const eventHandlers = {
  "node:dblclick": ({ node }: Node) => {
    doubleClickedNode(node);
  },
  "node:dragend": ({ node }: Node) => {
    stateSaved.value = false;
    nodeDraggedEnd(node);
  }
};
onMounted(() => {
  configs.node.selectable = true;
});
</script>
