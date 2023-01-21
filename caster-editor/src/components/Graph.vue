<template>
  <!-- Menu -->
  <Menu :graph="graph" :uuid="uuid" :selected-nodes="selectedNodes" :selected-edges="selectedEdges" />

  <!-- Graph -->
  <v-network-graph
    ref="graph" v-model:selected-nodes="selectedNodes" v-model:selected-edges="selectedEdges"
    class="graph" :nodes="graphStore.nodes()" :edges="graphStore.edges()" :configs="configs"
    :layouts="graphStore.layouts()" :event-handlers="eventHandlers"
  />

  <!-- Node Editor -->
  <div v-if="showEditor" ref="editorDom" class="node-data">
    <!-- TODO: this can be nil? -->
    <NodeEditor :node-uuid="selectedNodes[0]" />
  </div>

  <!-- Other Interface -->
  <div v-if="!showEditor" class="stats">
    <p>
      Nodes: {{ graphStore.graph.nodes.length }} &nbsp;
      Edges: {{ graphStore.graph.edges.length }}
    </p>
  </div>
</template>

<script lang="ts" setup>
import { ElMessage } from "element-plus";
import type { EventHandlers as GraphEventHandlers, Instance as GraphInstance } from "v-network-graph";
import type { Ref } from "vue";
import { nextTick } from "vue";
import { storeToRefs } from "pinia";
import { gsap } from "gsap";
import { useNodeStore } from "@/stores/NodeStore";
import { GraphSettings } from "@/assets/js/graphSettings";
import type { Scalars } from "@/graphql/graphql";
import { useGraphStore } from "@/stores/GraphStore";
import { useInterfaceStore } from "@/stores/InterfaceStore";

// Props
const props = defineProps<GraphProps>();

// Html
const editorDom = ref<HTMLElement>();

// Composables
const router = useRouter();

// Store
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

// Graph Manipulations
const centerClickLeftToEditor = (event: MouseEvent) => {
  if (!graph.value)
    return;

  // get click position
  const clickPos = {
    x: event.offsetX,
    y: event.offsetY
  };

  // get canvas size
  const { height: gHeight, width: gWidth } = graph.value.getSizes();

  // get editor width
  const editorWidth = editorDom.value?.offsetWidth || 0;

  // screen aim
  const aimPos = {
    x: (gWidth - editorWidth) / 2,
    y: gHeight / 2
  };

  // move by
  const moveBy = {
    x: aimPos.x - clickPos.x,
    y: aimPos.y - clickPos.y
  };

  const progress = {
    absolute: 0
  };

  let prevProgress = 0;

  const moveGraph = () => {
    const delta = progress.absolute - prevProgress;
    const shift = {
      x: moveBy.x * delta,
      y: moveBy.y * delta
    };

    graph.value?.panBy(shift);
    prevProgress = progress.absolute;
  };

  // animate
  gsap.to(progress, {
    absolute: 1,
    duration: 0.4,
    ease: "power3.inOut",
    onUpdate: () => {
      moveGraph();
    }
  });
};

const openNodeEditor = async (node: string) => {
  if (scriptCellsModified.value === true) {
    ElMessage({
      message: "Save or close scene before switching to another.",
      type: "error",
      customClass: "messages-editor"
    });
    return;
  }
  showEditor.value = true;
  // TODO:  display the loading animation

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
  "view:load": () => {
    graph.value?.fitToContents();
  },
  "node:dblclick": async ({ node, event }) => {
    openNodeEditor(node);
    await nextTick();
    centerClickLeftToEditor(event);
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
