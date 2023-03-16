<!-- eslint-disable vue/no-v-model-argument -->
<template>
  <div>
    <!-- Menu -->
    <Menu
      :graph="graph"
      :uuid="uuid"
      :selected-nodes="selectedNodes"
      :selected-edges="selectedEdges"
    />

    <!-- Graph -->
    <v-network-graph
      v-if="graphDataReady"
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

    <!-- Node Editor -->
    <div
      ref="editorDom"
      class="node-data"
      :class="{ 'node-data--open': showEditor }"
    >
      <NodeEditor class="node-editor-outer" />
    </div>

    <!-- Audio Selector -->
    <AudioSelector v-if="showAudioSelector" />

    <!-- Other Interface -->
    <div
      v-if="!showEditor"
      class="stats"
    >
      <p>
        Nodes: {{ graphInStore?.graph.nodes.length }} &nbsp; Edges:
        {{ graphInStore?.graph.edges.length }}
      </p>
    </div>

    <!-- Switch unsaved node dialog -->
    <ElDialog
      v-model="switchNodeDialog"
      title="Careful"
      width="25%"
      center
      lock-scroll
      :show-close="false"
    >
      <span>
        Unsaved changes in the editor! <br>
        Are you sure to switch node without saving?
      </span>
      <template #footer>
        <span class="dialog-footer">

          <ElButton
            text
            bg
            @click="switchWithoutSaving()"
          >
            Switch without saving
          </ElButton>
          <ElButton
            color="#ADFF00"
            @click="switchNodeDialog = false"
          >
            Cancel
          </ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>

<script lang="ts" setup>
export interface GraphProps {
  uuid: Scalars["UUID"];
}

import type {
  EventHandlers as GraphEventHandlers,
  Instance as GraphInstance,
} from "v-network-graph";
import { ref } from "vue";
import type { Ref } from "vue";
import { nextTick } from "vue";
import { storeToRefs } from "pinia";
import { gsap } from "gsap";
import { GraphSettings } from "@/assets/js/graphSettings";
import type { Scalars } from "@/graphql";
import { useGraphStore } from "@/stores/GraphStore";
import { useInterfaceStore } from "@/stores/InterfaceStore";
import { useNodeStore } from "@/stores/NodeStore";
import Menu from "./Menu.vue";
import NodeEditor from "./NodeEditor.vue";
import AudioSelector from  "./audioSelector/Selector.vue";

defineProps<GraphProps>();

// Html
const editorDom: Ref<HTMLElement | undefined> = ref(undefined);

// Store
const graphStore = useGraphStore();
const { graph: graphInStore, graphDataReady, selectedNodes, selectedEdges } = storeToRefs(graphStore);

const nodeStore = useNodeStore();
const { uuid: nodeUuid, scriptCellsModified } = storeToRefs(nodeStore);

const interfaceStore = useInterfaceStore();
const { showEditor, showAudioSelector } = storeToRefs(interfaceStore);

// Data
const graph: Ref<GraphInstance | undefined> = ref();

// Config
const configs = GraphSettings.standard;

// Graph Manipulations
const centerClickLeftToEditor = (event: MouseEvent) => {
  if (!graph.value) return;

  // get click position
  const clickPos = {
    x: event.offsetX,
    y: event.offsetY,
  };

  // get canvas size
  const { height: gHeight, width: gWidth } = graph.value.getSizes();

  // get editor width
  const editorWidth = editorDom.value?.offsetWidth || 0;

  // screen aim
  const aimPos = {
    x: (gWidth - editorWidth) / 2,
    y: gHeight / 2,
  };

  // move by
  const moveBy = {
    x: aimPos.x - clickPos.x,
    y: aimPos.y - clickPos.y,
  };

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
    },
  });
};

const openNodeEditor = () => {
  showEditor.value = true;
};


const eventHandlers: GraphEventHandlers = {
  // see https://dash14.github.io/v-network-graph/reference/events.html#events-with-event-handlers
  "view:load": () => {
    graph.value?.fitToContents();
  },
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  "node:dblclick": async ({ node, event }) => {
    nextNodeDoubleClicked.value = node;

    if (showEditor.value && scriptCellsModified.value) { // already open
      switchNodeDialog.value = true
      selectedNodes.value = [lastNodeDoubleClicked.value];
      return
    }

    lastNodeDoubleClicked.value = node;
    nodeUuid.value = node;

    openNodeEditor();
    await nextTick();
    centerClickLeftToEditor(event);
  },
  "node:dragend": (dragEvent: { [id: string]: { x: number; y: number } }) => {
    for (const p in dragEvent) {
      const draggedNode = graphInStore.value?.graph.nodes.find(
        (x) => x.uuid === p
      );
      if (draggedNode === undefined) {
        console.log("Could not find dragged Node in our local store");
        continue;
      }
      draggedNode.positionX = dragEvent[p].x;
      draggedNode.positionY = dragEvent[p].y;
      graphStore.updateNodePosition(draggedNode);
    }
  },
};

// Dialogs
const lastNodeDoubleClicked = ref<Scalars["UUID"]>("")
const nextNodeDoubleClicked = ref<Scalars["UUID"]>("")
const switchNodeDialog: Ref<boolean> = ref(false);

const switchWithoutSaving = () => {
  switchNodeDialog.value = false;
  scriptCellsModified.value = false;
  nodeUuid.value = nextNodeDoubleClicked.value;
  selectedNodes.value = [nextNodeDoubleClicked.value]
  lastNodeDoubleClicked.value = nextNodeDoubleClicked.value;
  openNodeEditor();
};
</script>
