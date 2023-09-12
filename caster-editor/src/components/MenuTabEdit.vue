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
import type { Graph } from "@/graphql";
import { useDeleteEdgeMutation, useDeleteNodeMutation } from "@/graphql";
import { useInterfaceStore } from "@/stores/InterfaceStore";
import { ElMessage } from "element-plus";
import { storeToRefs } from "pinia";
import { ref, type Ref } from "vue";
import DialogAddNode from "./DialogAddNode.vue";

export type GraphEdit = Pick<Graph, "uuid">;

defineProps<{
  graph: GraphEdit;
}>();

const { selectedNodeUUIDs, selectedEdgeUUIDs } = storeToRefs(
  useInterfaceStore(),
);

const showAddNodeDialog: Ref<boolean> = ref(false);

const deleteNodeMutation = useDeleteNodeMutation();
const deleteEdgeMutation = useDeleteEdgeMutation();

const removeSelection = async () => {
  await deleteSelectedEdgeUUIDs();
  // TODO: only works with a timeout?
  setTimeout(async () => {
    await deleteSelectedNodeUUIDs();
  }, 100);
  // await deleteSelectedNodeUUIDs();
  console.log("Deleted selected");
};

// deleteselectedEdgeUUIDs with callback
const deleteSelectedEdgeUUIDs = async () => {
  const deletePromises = selectedEdgeUUIDs.value.map(async (edgeUuid) => {
    const { error } = await deleteEdgeMutation.executeMutation({
      edgeUuid,
    });
    console.log("ran mutation");
    if (error) {
      ElMessage.error(`Could not delete edge ${edgeUuid}: ${error.message}`);
    }
    ElMessage.info(`Deleted edge ${edgeUuid}`);
  });

  // Wait for all delete promises to complete before returning
  await Promise.all(deletePromises);
};

const deleteSelectedNodeUUIDs = async () => {
  const deletePromises = selectedNodeUUIDs.value.map(async (nodeUuid) => {
    const { error } = await deleteNodeMutation.executeMutation({
      nodeUuid,
    });
    if (error) {
      ElMessage.error(`Could not delete node ${nodeUuid}: ${error.message}`);
    }
    ElMessage.info(`Deleted node ${nodeUuid}`);
  });

  // Wait for all delete promises to complete before returning
  await Promise.all(deletePromises);
};
</script>
