<!-- eslint-disable vue/no-v-model-argument -->
<script lang="ts" setup>
import DefaultNode from "@/components/FlowNodeDefault.vue";
import { ElMessage } from "element-plus";
import { ref, type Ref, watch } from "vue";
import { storeToRefs } from "pinia";
import { gsap } from "gsap";
import type { GraphSubscription, Scalars } from "@/graphql";
import { useUpdateNodeMutation, useCreateEdgeMutation } from "@/graphql";
import { useInterfaceStore } from "@/stores/InterfaceStore";
import DialogExitNode from "@/components/DialogExitNode.vue";
// import variables from "@/assets/scss/variables.module.scss";

import type {
  Node as GraphNodeF,
  Edge as GraphEdgeF,
  NodeDragEvent,
} from "@vue-flow/core";
import { VueFlow, useVueFlow } from "@vue-flow/core";

const { getSelectedEdges, getSelectedNodes } = useVueFlow({});

// watch(getNodes, (nodes) => console.log('nodes changed', nodes))
watch(getSelectedNodes, (nodes) => onSelectionChangeNodes(nodes));
watch(getSelectedEdges, (edges) => onSelectionChangeEdges(edges));

const props = defineProps<{
  graph: GraphSubscription["graph"];
}>();

const interfaceStore = useInterfaceStore();
const {
  showNodeEditor,
  selectedNodeUUIDs,
  selectedEdgeUUIDs,
  newScriptCellUpdates,
  selectedNodeForEditorUuid,
  vueFlowRef,
} = storeToRefs(interfaceStore);

watch(showNodeEditor, (visible) => {
  if (visible) {
    // graphPan(graphPanType.NodeEditor, lastNodeClick.value);
    // flowPan(graphPanType.NodeEditor);
  } else {
    // graphPan(graphPanType.Center, lastNodeClick.value);
    flowPan(graphPanType.Center);
  }
});

const lastPosition = ref<{ x: number; y: number }>({ x: 0, y: 0 });

const lastPanMove = ref({ x: 0, y: 0 });
enum graphPanType {
  NodeEditor = "NODE_EDITOR",
  Center = "CENTER",
}

const flowPan = (location: graphPanType) => {
  if (!vueFlowRef.value) return;

  const currentTransform = vueFlowRef.value.getTransform();
  lastPosition.value.x = currentTransform.x;
  lastPosition.value.y = currentTransform.y;

  // get canvas size
  console.log(vueFlowRef.value.dimensions);
  const { height: gHeight, width: gWidth } = vueFlowRef.value.dimensions;

  // screen aim
  let aimPos: { x: number; y: number };
  let moveBy: { x: number; y: number };

  // node
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

const updateNodeMutation = useUpdateNodeMutation();

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

  if (showNodeEditor.value && newScriptCellUpdates.value.size > 0) {
    showSwitchNodeDialog.value = true;
    return;
  }

  lastNodeDoubleClicked.value = uuid;
  selectedNodeUUIDs.value = [uuid];

  selectedNodeForEditorUuid.value = uuid;
  showNodeEditor.value = true;

  flowPan(graphPanType.NodeEditor);
};

const onSelectionChangeNodes = (nodes) => {
  console.log("nodes selection change");
  selectedNodeUUIDs.value = [];
  nodes.forEach((node) => {
    selectedNodeUUIDs.value.push(node.id);
  });
};

const onSelectionChangeEdges = (edges) => {
  console.log("edges selection change");
  selectedEdgeUUIDs.value = [];
  edges.forEach((edge) => {
    selectedEdgeUUIDs.value.push(edge.id);
  });
};

const connectionLineStyle = { stroke: "#000" };

function nodesF(): GraphNodeF[] {
  const n: GraphNodeF[] = [];

  props.graph.nodes.forEach((node) => {
    const graphNode: GraphNodeF = {
      label: node.name,
      type: "custom",
      data: {
        name: node.name,
        uuid: node.uuid,
        scriptCells: node.scriptCells,
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

function edgesF(): GraphEdgeF[] {
  const e: GraphEdgeF[] = [];
  props.graph.edges.forEach((edge) => {
    const graphEdge: GraphEdgeF = {
      id: edge.uuid,
      source: edge.inNode.uuid,
      target: edge.outNode.uuid,
      animated: true,
    };
    e.push(graphEdge);
  });
  return e;
}

// Dialogs
const lastNodeDoubleClicked = ref<Scalars["UUID"]>("");
const nextNodeDoubleClicked = ref<Scalars["UUID"]>("");
const showSwitchNodeDialog: Ref<boolean> = ref(false);

const createEdgeMutation = useCreateEdgeMutation();

// this runs if mouse is released on connection
const onConnect = async (connection) => {
  // console.log(connection);

  const nodeOutUuid = connection.target;
  const nodeInUuid = connection.source;

  const { error } = await createEdgeMutation.executeMutation({
    nodeInUuid,
    nodeOutUuid,
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
        :nodes="nodesF()"
        :edges="edgesF()"
        :nodes-connectable="true"
        :connection-line-style="connectionLineStyle"
        :delete-key-code="'null'"
        @node-drag-stop="onNodeDragStop"
        @connect="onConnect"
      >
        <template #node-custom="{ data }">
          <DefaultNode
            :data="data"
            @dblclick="onNodeDoubleClick"
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
          await interfaceStore.executeScriptCellUpdates();
          selectedNodeForEditorUuid = nextNodeDoubleClicked;
          showSwitchNodeDialog = false;
        }
      "
      @no-save="
        () => {
          interfaceStore.resetScriptCellUpdates();
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
  // height: calc(50vh);
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
