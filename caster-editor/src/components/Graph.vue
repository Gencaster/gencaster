<!-- eslint-disable vue/no-v-model-argument -->
<script lang="ts" setup>
import type {
  EventHandlers as GraphEventHandlers,
  Edge as GraphEdge,
  Edges as GraphEdges,
  Node as GraphNode,
  Nodes as GraphNodes,
} from "v-network-graph";

import DefaultNode from "@/components/FlowNodeDefault.vue";
import { ElMessage } from "element-plus";
import { ref, type Ref, watch, nextTick } from "vue";
import { storeToRefs } from "pinia";
import { gsap } from "gsap";
import type { GraphSubscription, Scalars } from "@/graphql";
import { useUpdateNodeMutation, useCreateEdgeMutation } from "@/graphql";
import { useInterfaceStore } from "@/stores/InterfaceStore";
import * as vNG from "v-network-graph";
import { VNetworkGraph } from "v-network-graph";
import variables from "@/assets/scss/variables.module.scss";
import DialogExitNode from "@/components/DialogExitNode.vue";

import type {
  Node as GraphNodeF,
  Edge as GraphEdgeF,
  NodeDragEvent,
} from "@vue-flow/core";
import { VueFlow, useVueFlow } from "@vue-flow/core";

const { getSelectedEdges, getSelectedNodes, getTransform, viewport } =
  useVueFlow({});

// watch(getNodes, (nodes) => console.log('nodes changed', nodes))
watch(getSelectedNodes, (nodes) => onSelectionChangeNodes(nodes));
watch(getSelectedEdges, (edges) => onSelectionChangeEdges(edges));

const props = defineProps<{
  graph: GraphSubscription["graph"];
}>();

const interfaceStore = useInterfaceStore();
const {
  showNodeEditor,
  vNetworkGraph,
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

const lastNodeClick = ref<MouseEvent>();
const lastPanMove = ref({ x: 0, y: 0 });
enum graphPanType {
  NodeEditor = "NODE_EDITOR",
  Center = "CENTER",
}

const graphPan = (location: graphPanType, event?: MouseEvent) => {
  if (!vNetworkGraph.value) return;

  // get click position
  const clickPos = {
    x: event?.offsetX || 0,
    y: event?.offsetY || 0,
  };

  // get canvas size
  const { height: gHeight, width: gWidth } = vNetworkGraph.value.getSizes();

  // screen aim
  let aimPos: { x: number; y: number };
  let moveBy: { x: number; y: number };

  switch (location) {
    case graphPanType.NodeEditor:
      // const editorWidth = document.getElementsByClassName('node-editor')[0]?.clientWidth || 0;
      const editorWidth = 800; // this needs to be hard coded for transition purposes
      aimPos = {
        x: (gWidth - editorWidth) / 2,
        y: (gHeight / 2) * 0.9, // 0.9 to visually center vertical
      };

      moveBy = {
        x: aimPos.x - clickPos.x,
        y: aimPos.y - clickPos.y,
      };

      lastPanMove.value = moveBy;
      break;
    case graphPanType.Center:
      aimPos = {
        x: gWidth / 2,
        y: (gHeight / 2) * 0.9, // 0.9 to visually center vertical
      };

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

    vNetworkGraph.value?.panBy(shift);
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

      // console.log('starting position');
      // console.log(vueFlowRef.value.getTransform());
      // console.log('node Position');
      // console.log(nodePosition);
      // console.log('moveby');
      // console.log(moveBy);
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
  // const { height: gHeight, width: gWidth } = vueFlowRef.value.getSizes();

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

const panToFirstNode = async () => {
  const nodes = props.graph.nodes;
  const firstNode = nodes.find((x) => x.name == "Start") || nodes[0];
  const viewBox = vNetworkGraph.value?.getViewBox() || {
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
  };

  await nextTick();
  vNetworkGraph.value?.panTo({
    x: -firstNode.positionX + Math.abs(viewBox.left - viewBox.right) / 2,
    y:
      -firstNode.positionY + (Math.abs(viewBox.top - viewBox.bottom) / 2) * 0.9,
  });
};

const updateNodeMutation = useUpdateNodeMutation();

const eventHandlers: GraphEventHandlers = {
  // see https://dash14.github.io/v-network-graph/reference/events.html#events-with-event-handlers
  "view:load": () => {
    panToFirstNode();
  },
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  "node:dblclick": async ({ node, event }) => {
    nextNodeDoubleClicked.value = node;

    if (showNodeEditor.value && newScriptCellUpdates.value.size > 0) {
      showSwitchNodeDialog.value = true;
      return;
    }

    lastNodeDoubleClicked.value = node;
    selectedNodeUUIDs.value = [node];

    showNodeEditor.value = true;
    selectedNodeForEditorUuid.value = node;
    lastNodeClick.value = event;
  },
  "node:dragend": (dragEvent: { [id: string]: { x: number; y: number } }) => {
    for (const p in dragEvent) {
      const draggedNode = props.graph.nodes.find((x) => x.uuid === p);
      if (draggedNode === undefined) {
        console.log(`Dragged unknown node ${p}`);
        continue;
      }

      updateNodeMutation.executeMutation({
        nodeUuid: draggedNode.uuid,
        positionX: dragEvent[p].x,
        positionY: dragEvent[p].y,
      });
    }
  },
};

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
  console.log("selection change");
  selectedNodeUUIDs.value = [];
  nodes.forEach((node) => {
    selectedNodeUUIDs.value.push(node.id);
  });
};

const onSelectionChangeEdges = (edges) => {
  console.log("selection change");
  selectedEdgeUUIDs.value = [];
  edges.forEach((edge) => {
    selectedEdgeUUIDs.value.push(edge.id);
  });
};

/*
  transforms the edges, nodes and layout from our StoryGraph model to
  v-network-graph model. Maybe this can be done in a nicer,
  two way support via urql as some kind of type transformation?
*/
function nodes(): GraphNodes {
  const n: GraphNodes = {};
  props.graph.nodes.forEach((node) => {
    const graphNode: GraphNode = {
      name: node.name,
      color: node.color,
      scriptCells: node.scriptCells,
    };
    n[node.uuid] = graphNode;
  });
  return n;
}

// Flow
// const nodesF = ref([
//   { id: '1', label: 'Start', position: { x: 250, y: 5 } },
//   { id: '2', label: 'Node 1', position: { x: 100, y: 100 } },
//   { id: '3', label: 'Node 2', position: { x: 400, y: 100 } },
// ]);

// const edgesF = ref([
//   // { id: 'e1-3', source: '1', target: '2', animated: true },
//   // { id: 'e1-2', source: '2', target: '3', animated: true },
// ]);

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

function edges(): GraphEdges {
  const e: GraphEdges = {};
  props.graph.edges.forEach((edge) => {
    const graphEdge: GraphEdge = {
      source: edge.inNode.uuid,
      target: edge.outNode.uuid,
    };
    e[edge.uuid] = graphEdge;
  });
  return e;
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

function layouts(): GraphNodes {
  const n: GraphNodes = {};
  props.graph.nodes.forEach((node) => {
    const graphNode: GraphNode = {
      x: node.positionX,
      y: node.positionY,
    };
    n[node.uuid] = graphNode;
  });
  const layout = {
    nodes: n,
  };
  return layout;
}

// Dialogs
const lastNodeDoubleClicked = ref<Scalars["UUID"]>("");
const nextNodeDoubleClicked = ref<Scalars["UUID"]>("");
const showSwitchNodeDialog: Ref<boolean> = ref(false);

const graphSettings = {
  standard: vNG.defineConfigs({
    node: {
      selectable: true,
      normal: {
        type: "circle",
        radius: 16,
        strokeWidth: 0,
        color: variables.grey,
      },
      hover: {
        type: "circle",
        radius: 16,
        strokeWidth: 0,
        color: variables.greenLight,
      },
      selected: {
        type: "circle",
        radius: 16,
        strokeWidth: 0,
        color: variables.greenLight,
      },
      label: {
        fontSize: 15,
        fontFamily: "arial",
        color: variables.black,
        margin: 5,
        background: {
          visible: true,
          color: variables.white08,
          padding: {
            vertical: 1,
            horizontal: 4,
          },
          borderRadius: 2,
        },
      },
      focusring: { visible: false },
      zOrder: {
        enabled: true, // whether the z-order control is enable or not. default: false
        bringToFrontOnHover: true, // whether to bring to front on hover.    default: true
        bringToFrontOnSelected: true, // whether to bring to front on selected. default: true
      },
    },
    edge: {
      selectable: true,
      normal: {
        width: 3,
        color: "black",
        dasharray: 0,
        animationSpeed: 5,
        linecap: "square",
        animate: false,
      },
      hover: {
        width: 4,
        color: variables.greenLight,
        dasharray: "0",
        linecap: "square",
        animate: false,
      },
      selected: {
        width: 3,
        color: variables.greenLight,
        dasharray: "0",
        linecap: "square",
        animate: false,
      },
      gap: 5,
      // type: "straight",
      type: "curve",
      // gap: 40,
      margin: 8, // margin between the edge and the node
      marker: {
        source: {
          type: "none",
          width: 4,
          height: 4,
          margin: -1,
          units: "strokeWidth",
          color: null,
        },
        target: {
          type: "arrow",
          width: 4,
          height: 6,
          margin: -1,
          units: "strokeWidth",
          color: null,
        },
      },
      zOrder: {
        enabled: true, // whether the z-order control is enable or not. default: false
        bringToFrontOnHover: true, // whether to bring to front on hover.    default: true
        bringToFrontOnSelected: true, // whether to bring to front on selected. default: true
      },
    },
    view: {
      zoomEnabled: false,
      grid: {
        visible: false,
        interval: 30,
        thickIncrements: 0,
        line: {
          color: "#F5F5F5",
          width: 1,
          dasharray: 0,
        },
        thick: {
          color: "#F5F5F5",
          width: 1,
          dasharray: 0,
        },
      },
      // layoutHandler: new vNG.GridLayout({ grid: 30 })
    },
  }),
};

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

.graph {
  position: relative;
  width: 100%;
  height: calc(50vh - 64px);
  background-color: yellow;
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
