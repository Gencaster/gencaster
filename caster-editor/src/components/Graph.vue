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
              {{ graphStore.graph.name }}
            </span>
          </div>
          <div class="menu-items right">
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
        Nodes: {{ graphStore.graph.nodes.length }} &nbsp;
        Edges: {{ graphStore.graph.edges.length }}
      </p>
    </div>

    <!-- Dialogs -->
    <!-- Are you sure to delete? -->
    <el-dialog v-model="deleteDialogVisible" title="Careful" width="25%" center lock-scroll :show-close="false">
      <span>
        Are you sure to delete Scene "{{ graph?.nodes[selectedNodes[0]].name }}"?
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
import type { EventHandlers as GraphEventHandlers, Instance as GraphInstance } from "v-network-graph";
import type { Ref } from "vue";
import { storeToRefs } from "pinia";
import { computed } from "vue";
import { useNodeStore } from "../stores/NodeStore";
import { GraphSettings } from "@/assets/js/graphSettings";
import type { Scalars } from "@/graphql/graphql";
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
const { scriptCellsModified } = storeToRefs(nodeStore);
const { showEditor } = storeToRefs(useInterfaceStore());

interface GraphProps {
  uuid: Scalars["UUID"]
}

// Data
const graph = ref<GraphInstance>();
const selectedNodes: Ref<string[]> = ref([]);
const selectedEdges: Ref<string[]> = ref([]);

// Config
const configs = GraphSettings.standard;

// Interface
const deleteDialogVisible = ref(false);
const exitDialogVisible = ref(false);

// Computed
const hideConnectionButton = computed(() => {
  return selectedNodes.value.length !== 2;
});

const hideRemoveButton = computed(() => {
  if ((selectedNodes.value.length === 0 && selectedEdges.value.length === 0) || (selectedNodes.value.length === 0 && selectedEdges.value.length === 0))
    return true;
  else if ((selectedNodes.value.length > 1 || selectedEdges.value.length > 1))
    return true;
  else return false;
});

const addNode = async () => {
  if (!graph.value) {
    console.error("can't add node since graph not defined", graph);
    return;
  }

  const { height, width } = graph.value.getSizes();
  const centerPosition = graph.value.translateFromDomToSvgCoordinates({ x: width / 2, y: height / 2 });

  await graphStore.addNode({
    graphUuid: props.uuid,
    name: "new node",
    color: "primary",
    positionX: centerPosition.x,
    positionY: centerPosition.y
  });
};

const deleteSelectedNodes = async () => {
  deleteDialogVisible.value = false;
  for (const nodeUuid of selectedNodes.value)
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
  // ui should display the loading animation
  // so it is ok to first display the editor and then
  // load the data
  //
  // we moved this from the node editor component to here
  // because the destroy mechanism lead to some strange
  // quirks when running async code
  await nodeStore.getNode(selectedNodes.value[0]);
};

const eventHandlers: GraphEventHandlers = {
  // see https://dash14.github.io/v-network-graph/reference/events.html#events-with-event-handlers
  "node:dblclick": ({ node }) => {
    openNodeEditor(node);
  },
  "node:dragend": (dragEvent: { [id: string]: { x: number; y: number } }) => {
    for (const p in dragEvent) {
      const draggedNode = graphStore.graph.nodes.find(x => x.uuid === p);
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
