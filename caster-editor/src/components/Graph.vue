<template>
  <div class="index-page">
    <!-- Menu -->
    <div>
      <div class="menu menu-edit">
        <div class="level level-1">
          <div class="menu-items left">
            <el-radio-group v-model="menuLevel1">
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
          <div v-if="menuLevel1 === 'edit'" class="left">
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
          <div v-if="menuLevel1 === 'test'" />
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
  </div>
</template>

<script lang="ts" setup>
import type { Edges, Node, Nodes } from "v-network-graph";
import type { Ref } from "vue";
import { GraphSettings } from "../assets/js/graphSettings";
import type { Graph, ScriptCell } from "../graphql/graphql";
import { transformEdges, transformLayout, transformNodes } from "../tools/typeTransformers";

interface GraphProps {
  graph: Graph
}
// Props
const props = defineProps<GraphProps>();

// Data
const menuLevel1 = ref("edit");
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

// Methods
const addEdge = () => {};
const addNode = () => {};
const exitEditing = () => {};
const refresh = () => {};
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
