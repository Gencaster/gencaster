<template>
  <div>
    <button
      class="unstyled"
      @click="showAddNodeDialog = true"
    >
      Add Scene
    </button>
    <button
      class="unstyled"
      @click="removeSelection()"
    >
      Remove Selected
    </button>
    <DialogAddNode
      v-if="showAddNodeDialog"
      :graph-uuid="graph.uuid"
      @closed="showAddNodeDialog = false"
    />
  </div>
</template>

<script setup lang="ts">
import type { Graph, Node } from "@/graphql";
import { useDeleteEdgeMutation, useDeleteNodeMutation } from "@/graphql";
import { useInterfaceStore } from "@/stores/InterfaceStore";
import { ElMessage } from "element-plus";
import { storeToRefs } from "pinia";
import { ref, type Ref } from "vue";
import DialogAddNode from "./DialogAddNode.vue";

export type GraphEdit = Pick<Graph, "uuid"> & {
  nodes: Pick<Node, "uuid" | "isEntryNode">[];
};

const props = defineProps<{
  graph: GraphEdit;
}>();

const { selectedNodeUUIDs, selectedEdgeUUIDs } = storeToRefs(
  useInterfaceStore(),
);

const showAddNodeDialog: Ref<boolean> = ref(false);

const deleteNodeMutation = useDeleteNodeMutation();
const deleteEdgeMutation = useDeleteEdgeMutation();

const checkIfNodeEntry = (nodeUuid: string): boolean => {
  return (
    props.graph.nodes.find((x) => x.uuid === nodeUuid)?.isEntryNode ?? false
  );
};

const removeSelection = async () => {
  console.log("Removing selection");

  // deleting edges first
  selectedEdgeUUIDs.value.forEach(async (edgeUuid) => {
    const { error } = await deleteEdgeMutation.executeMutation({
      edgeUuid,
    });
    if (error) {
      ElMessage.error(`Could not delete edge ${edgeUuid}: ${error.message}`);
    } else {
      ElMessage.info(`Deleted edge ${edgeUuid}`);
    }
  });

  selectedNodeUUIDs.value.forEach(async (nodeUuid) => {
    // compare if to props.graph.nodes and find isEntryNode
    if (checkIfNodeEntry(nodeUuid)) {
      ElMessage.error(`Cannot delete entry node.`);
      return;
    }

    const { error } = await deleteNodeMutation.executeMutation({
      nodeUuid,
    });
    if (error) {
      ElMessage.error(`Could not delete node ${nodeUuid}: ${error.message}`);
    } else {
      ElMessage.info(`Deleted node ${nodeUuid}`);
    }
  });
};
</script>
