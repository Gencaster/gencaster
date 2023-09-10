<!-- eslint-disable vue/no-v-model-argument -->
<script lang="ts" setup>
import { ElMessage } from "element-plus";
import NodeDefault from "@/components/FlowNodeDefault.vue";
import { ref, type Ref, watch } from "vue";
import { storeToRefs } from "pinia";
import { gsap } from "gsap";
import type { GraphSubscription, Scalars } from "@/graphql";
import { useUpdateNodeMutation, useCreateEdgeMutation } from "@/graphql";
import { useInterfaceStore } from "@/stores/InterfaceStore";
import DialogExitNode from "@/components/DialogExitNode.vue";
import type {
  Node as GraphNode,
  Edge as GraphEdge,
  NodeDragEvent,
  Connection,
} from "@vue-flow/core";
import { VueFlow, useVueFlow } from "@vue-flow/core";

// mutations
const updateNodeMutation = useUpdateNodeMutation();
const createEdgeMutation = useCreateEdgeMutation();

// types
enum graphPanType {
  NodeEditor = "NODE_EDITOR",
  Center = "CENTER",
}

// store
const interfaceStore = useInterfaceStore();
const {
  showNodeEditor,
  selectedNodeUUIDs,
  selectedEdgeUUIDs,
  unsavedNodeChanges,
  selectedNodeForEditorUuid,
  vueFlowRef,
} = storeToRefs(interfaceStore);
const { getSelectedEdges, getSelectedNodes } = useVueFlow({});

// props
const props = defineProps<{
  graph: GraphSubscription["graph"];
}>();

// watchers
watch(getSelectedNodes, (nodes) => onSelectionChangeNodes(nodes));
watch(getSelectedEdges, (edges) => onSelectionChangeEdges(edges));
watch(showNodeEditor, (visible) => {
  if (!visible) {
    flowPan(graphPanType.Center);
  }
});

// vars
const lastPosition = ref<{ x: number; y: number }>({ x: 0, y: 0 });
const lastPanMove = ref({ x: 0, y: 0 });
const lastNodeDoubleClicked = ref<Scalars["UUID"]>("");
const nextNodeDoubleClicked = ref<Scalars["UUID"]>("");
const showSwitchNodeDialog: Ref<boolean> = ref(false);

// styling
const connectionLineStyle = { stroke: "#000" };

//functions
function nodes(): GraphNode[] {
  const n: GraphNode[] = [];

  props.graph.nodes.forEach((node) => {
    const graphNode: GraphNode = {
      label: node.name,
      type: "custom",
      data: {
        name: node.name,
        uuid: node.uuid,
        inNodeDoors: node.inNodeDoors,
        outNodeDoors: node.outNodeDoors,
      },
      id: node.uuid,
      position: {
        x: node.positionX,
        y: node.positionY,
      },
    };
    n.push(graphNode);
  });
  return n;
}

function edges(): GraphEdge[] {
  const e: GraphEdge[] = [];
  props.graph.edges.forEach((edge) => {
    // @todo make inNodeDoor non-nullable
    if (edge.inNodeDoor && edge.outNodeDoor) {
      const graphEdge: GraphEdge = {
        id: edge.uuid,
        source: edge.outNodeDoor.node.uuid,
        sourceHandle: edge.outNodeDoor.uuid,
        target: edge.inNodeDoor.node.uuid,
        targetHandle: edge.inNodeDoor.uuid,
        animated: true,
      };
      e.push(graphEdge);
    }
  });
  return e;
}

const onNodeDragStop = (nodeDragEvent: NodeDragEvent) => {
  const draggedNode = props.graph.nodes.find(
    (x) => x.uuid === nodeDragEvent.node.id,
  );

  if (draggedNode === undefined) {
    console.log(`Dragged unknown node ${nodeDragEvent.node.label}`);
    return;
  }

  updateNodeMutation.executeMutation({
    nodeUuid: draggedNode.uuid,
    positionX: nodeDragEvent.node.computedPosition.x,
    positionY: nodeDragEvent.node.computedPosition.y,
  });
};

const onNodeDoubleClick = (uuid: string) => {
  nextNodeDoubleClicked.value = uuid;

  if (showNodeEditor.value && unsavedNodeChanges.value) {
    showSwitchNodeDialog.value = true;
    return;
  }

  lastNodeDoubleClicked.value = uuid;
  selectedNodeUUIDs.value = [uuid];

  selectedNodeForEditorUuid.value = uuid;
  showNodeEditor.value = true;

  flowPan(graphPanType.NodeEditor);
};

const onSelectionChangeNodes = (nodes: Array<GraphNode>) => {
  console.log("nodes selection change");
  selectedNodeUUIDs.value = [];
  nodes.forEach((node) => {
    selectedNodeUUIDs.value.push(node.id);
  });
};

const onSelectionChangeEdges = (edges: Array<GraphEdge>) => {
  console.log("edges selection change");
  selectedEdgeUUIDs.value = [];
  edges.forEach((edge) => {
    selectedEdgeUUIDs.value.push(edge.id);
  });
};

const flowPan = (location: graphPanType) => {
  if (!vueFlowRef.value) return;

  const currentTransform = vueFlowRef.value.getTransform();
  lastPosition.value.x = currentTransform.x;
  lastPosition.value.y = currentTransform.y;

  // get canvas size
  const { height: gHeight, width: gWidth } = vueFlowRef.value.dimensions;

  // screen aim
  let aimPos: { x: number; y: number };
  let moveBy: { x: number; y: number };

  // get node
  const node = vueFlowRef.value.findNode(selectedNodeForEditorUuid.value);
  const nodePosition = node?.position || { x: 0, y: 0 };
  const nodeDimensions = node?.dimensions || { width: 0, height: 0 };

  switch (location) {
    case graphPanType.NodeEditor:
      const editorWidth = 800; // this needs to be hard coded for transition purposes

      aimPos = {
        x: (gWidth - editorWidth) / 2,
        y: (gHeight / 2) * 0.9, // 0.9 to visually center vertical
      };

      moveBy = {
        x:
          aimPos.x -
          nodePosition.x -
          nodeDimensions.width / 2 -
          currentTransform.x,
        y:
          aimPos.y -
          nodePosition.y -
          nodeDimensions.height / 2 -
          currentTransform.y,
      };

      lastPanMove.value = moveBy;
      break;
    case graphPanType.Center:
      moveBy = {
        x: -lastPanMove.value.x,
        y: -lastPanMove.value.y,
      };
      break;
  }

  const progress = {
    absolute: 0,
  };

  let prevProgress = 0;

  const moveGraph = () => {
    const delta = progress.absolute - prevProgress;
    const shift = {
      x: moveBy.x * delta,
      y: moveBy.y * delta,
    };

    vueFlowRef.value?.panBy(shift);
    prevProgress = progress.absolute;
  };

  // animate
  gsap.to(progress, {
    absolute: 1,
    duration: 0.3,
    ease: "power3.inOut",
    onUpdate: () => {
      moveGraph();
    },
  });
};

// this runs if mouse is released on connection
const onConnect = async (connection: Connection) => {
  const nodeDoorOutUuid = connection.sourceHandle;
  const nodeDoorInUuid = connection.targetHandle;

  const { error } = await createEdgeMutation.executeMutation({
    nodeDoorInUuid,
    nodeDoorOutUuid,
  });
  if (error) {
    ElMessage.error(`Could not create edge: ${error.message}`);
  }
  ElMessage.success(`Created new edge`);
};
</script>

<template>
  <div>
    <div class="flow-graph">
      <VueFlow
        ref="vueFlowRef"
        :default-zoom="1"
        :max-zoom="1"
        :min-zoom="1"
        :nodes="nodes()"
        :edges="edges()"
        :connection-line-style="connectionLineStyle"
        fit-view-on-init
        :nodes-connectable="true"
        @node-drag-stop="onNodeDragStop"
        @connect="onConnect"
      >
        <template #node-custom="{ data }">
          <NodeDefault
            :data="data"
            :connectable="true"
            :selected="selectedNodeUUIDs.includes(data.uuid)"
            @dblclick="() => onNodeDoubleClick(data.uuid)"
          />
        </template>
      </VueFlow>
    </div>
    <div
      v-if="!showNodeEditor"
      class="stats"
    >
      <p>
        Nodes: {{ graph.nodes.length }} &nbsp; Edges:
        {{ graph.edges.length }}
      </p>
    </div>
    <DialogExitNode
      v-if="showSwitchNodeDialog"
      @cancel="
        () => {
          showSwitchNodeDialog = false;
        }
      "
      @save="
        async () => {
          await interfaceStore.executeUpdates();
          selectedNodeForEditorUuid = nextNodeDoubleClicked;
          showSwitchNodeDialog = false;
        }
      "
      @no-save="
        () => {
          interfaceStore.resetUpdates();
          selectedNodeForEditorUuid = nextNodeDoubleClicked;
          showSwitchNodeDialog = false;
        }
      "
    />
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/scss/variables.module.scss";

.flow-graph {
  --vf-node-bg: white;
  --vf-node-text: $black;
  --vf-connection-path: $black;
  --vf-handle: $grey-dark;

  position: relative;
  width: 100%;
  height: calc(100vh - 64px);
  background-color: light-grey;
}

.stats {
  position: fixed;
  bottom: 10px;
  right: 15px;

  p {
    margin: 0;
  }
}
</style>
