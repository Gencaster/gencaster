<template>
  <div>
    <button
      class="unstyled"
      @click="createNode()"
    >
      Add Scene
    </button>
    <button
      class="unstyled"
      :class="{ lighter: hideConnectionButton }"
      @click="createEdge()"
    >
      Add Connection
    </button>
    <button
      class="unstyled"
      :class="{ lighter: hideRemoveButton }"
      @click="removeSelection()"
    >
      Remove
    </button>
  </div>
</template>

<script setup lang="ts">
import type { Graph } from '@/graphql';
import { useCreateNodeMutation, useCreateEdgeMutation, useDeleteEdgeMutation, useDeleteNodeMutation } from "@/graphql";
import { useInterfaceStore } from "@/stores/InterfaceStore";
import { ElMessage } from "element-plus"
import { storeToRefs } from 'pinia';


export type GraphEdit = Pick<Graph, 'uuid'>

const props = defineProps<{
  graph: GraphEdit
}>();

const { selectedNodeUUIDs, selectedEdgeUUIDs, vNetworkGraph } = storeToRefs(useInterfaceStore());

const createNodeMutation = useCreateNodeMutation();
const createNode = async () => {
  let positionX = 0;
  let positionY = 0;
  if(vNetworkGraph.value) {
    const { height, width } = vNetworkGraph.value.getSizes();
    const pos = vNetworkGraph.value.translateFromDomToSvgCoordinates({
      x: width/2,
      y: height/2,
    });
    positionX = pos.x;
    positionY = pos.y;
  }

  const { error } = await createNodeMutation.executeMutation({
    name: "new scene",
    color: "primary",
    positionX,
    positionY,
    graphUuid: props.graph.uuid,
  });
  if(error) {
    alert(`Could not create node: ${error.message}`)
  }
}

const deleteNodeMutation = useDeleteNodeMutation();
const deleteEdgeMutation = useDeleteEdgeMutation();

const removeSelection = async () => {
  if (selectedNodeUUIDs.value.length==0 && selectedEdgeUUIDs.value.length == 0) {
    displayError("Please select max one scene or one connection.");
  }

  selectedNodeUUIDs.value.forEach(async (nodeUuid) => {
    console.log(`Delete node ${nodeUuid}`);
    const { error } = await  deleteNodeMutation.executeMutation({
      nodeUuid,
    });
    if(error) {
      displayError(`Could not delete node ${nodeUuid}: ${error.message}`);
    }
  });

  selectedEdgeUUIDs.value.forEach(async (edgeUuid) => {
    console.log(`Delete node ${edgeUuid}`);
    const { error } = await  deleteEdgeMutation.executeMutation({
      edgeUuid,
    });
    if(error) {
      displayError(`Could not delete edge ${edgeUuid}: ${error.message}`);
    }
  });
}

const displayError = async(message: string) => {
  ElMessage({
      message: message,
      type: "error",
      customClass: "messages-editor",
    });
}

const createEdgeMutation = useCreateEdgeMutation();
const createEdge = async () => {
  if (selectedNodeUUIDs.value.length !== 2) {
    displayError("requires exactly 2 scenes selected.");
    return;
  }
  const [nodeInUuid, nodeOutUuid] = selectedNodeUUIDs.value;
  const { error } = await createEdgeMutation.executeMutation({
    nodeInUuid,
    nodeOutUuid,
  });
  if(error) {
    alert(`Could not create edege: ${error.message}`);
  }
}

// is it maybe better to always have this
// clickable and show an error message on how you can use it?
// otherwise people may not know how to activate the buttons
const hideConnectionButton = false;
const hideRemoveButton = false;

</script>
