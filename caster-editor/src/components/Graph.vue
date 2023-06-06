<!-- eslint-disable vue/no-v-model-argument -->
<script lang="ts" setup>

import type {
  EventHandlers as GraphEventHandlers,
  Edge as GraphEdge,
  Edges as GraphEdges,
  Node as GraphNode,
  Nodes as GraphNodes,
} from "v-network-graph";

import { ref, type Ref, watch } from "vue";
import { storeToRefs } from "pinia";
import { gsap } from "gsap";
import type { GraphSubscription, Scalars } from "@/graphql";
import { useUpdateNodeMutation } from "@/graphql";
import { useInterfaceStore } from "@/stores/InterfaceStore";
import * as vNG from "v-network-graph";
import { VNetworkGraph } from "v-network-graph";
import variables from "@/assets/scss/variables.module.scss";

const props = defineProps<{
  graph: GraphSubscription['graph']
}>();

// Store
const {
  showNodeEditor,
  vNetworkGraph,
  selectedNodeUUIDs,
  selectedEdgeUUIDs,
  scriptCellsModified,
} = storeToRefs(useInterfaceStore());



watch(showNodeEditor, (visible) => {
  if (visible) {
    graphPan(graphPanType.NodeEditor, lastNodeClick.value);
  } else {
    graphPan(graphPanType.Center, lastNodeClick.value);
  }
});

const lastNodeClick = ref<MouseEvent>();
const lastPanMove = ref({x:0, y:0});
enum graphPanType {
  NodeEditor = 'NODEEDITOR',
  Center = 'CENTER',
}

const graphPan = (location: graphPanType, event?: MouseEvent) => {
  if (!vNetworkGraph.value) return;

  // get click position
  const clickPos = {
    x: event.offsetX || 0,
    y: event.offsetY || 0,
  };


  // get canvas size
  const { height: gHeight, width: gWidth } = vNetworkGraph.value.getSizes();

  // screen aim
  let aimPos: { x: number; y: number };
  let moveBy: { x: number; y: number };

  switch (location) {
    case graphPanType.NodeEditor:
      const editorWidth = document.getElementsByClassName('node-editor')[0]?.clientWidth || 0;
      aimPos = {
        x: (gWidth - editorWidth) / 2,
        y: gHeight / 2 * 0.9, // 0.9 to visually center vertical
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
        y: gHeight / 2 * 0.9, // 0.9 to visually center vertical
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
    duration: 0.4,
    ease: "power3.inOut",
    onUpdate: () => {
      moveGraph();
    },
  });
};

const updateNodeMutation = useUpdateNodeMutation();

const eventHandlers: GraphEventHandlers = {
  // see https://dash14.github.io/v-network-graph/reference/events.html#events-with-event-handlers
  "view:load": () => {
    vNetworkGraph.value?.fitToContents();
  },
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  "node:dblclick": async ({ node, event }) => {
    nextNodeDoubleClicked.value = node;

    if (showNodeEditor.value && scriptCellsModified.value) { // already open
      switchNodeDialog.value = true;
      selectedNodeUUIDs.value = [lastNodeDoubleClicked.value];
      return;
    }

    lastNodeDoubleClicked.value = node;
    selectedNodeUUIDs.value = [node];

    showNodeEditor.value = true;
    lastNodeClick.value = event;
  },
  "node:dragend": (dragEvent: { [id: string]: { x: number; y: number } }) => {
    for (const p in dragEvent) {

      const draggedNode = props.graph.nodes.find(
        (x) => x.uuid === p,
      );
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
const switchNodeDialog: Ref<boolean> = ref(false);

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
</script>

<template>
  <div>
    <VNetworkGraph
      ref="vNetworkGraph"
      v-model:selected-nodes="selectedNodeUUIDs"
      v-model:selected-edges="selectedEdgeUUIDs"
      class="graph"
      :nodes="nodes()"
      :edges="edges()"
      :configs="graphSettings.standard"
      :layouts="layouts()"
      :event-handlers="eventHandlers"
    />

    <div
      v-if="!showNodeEditor"
      class="stats"
    >
      <p>
        Nodes: {{ graph.nodes.length }} &nbsp; Edges:
        {{ graph.edges.length }}
      </p>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/scss/variables.module.scss';

.graph {
  position: relative;
  width: 100%;
  height: calc(100vh - 64px);
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
