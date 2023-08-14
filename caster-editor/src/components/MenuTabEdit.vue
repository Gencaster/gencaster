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
      @click="createEdge()"
    >
      Add Connection
    </button>
    <button
      class="unstyled"
      @click="removeSelection()"
    >
      Remove
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
import {
  useCreateEdgeMutation,
  useDeleteEdgeMutation,
  useDeleteNodeMutation,
} from "@/graphql";
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
  console.log("Removing selection");

  // deleting edges first
  selectedEdgeUUIDs.value.forEach(async (edgeUuid) => {
    const { error } = await deleteEdgeMutation.executeMutation({
      edgeUuid,
    });
    if (error) {
      ElMessage.error(`Could not delete edge ${edgeUuid}: ${error.message}`);
    }
    ElMessage.info(`Deleted edge ${edgeUuid}`);
  });

  selectedNodeUUIDs.value.forEach(async (nodeUuid) => {
    const { error } = await deleteNodeMutation.executeMutation({
      nodeUuid,
    });
    if (error) {
      ElMessage.error(`Could not delete node ${nodeUuid}: ${error.message}`);
    }
    ElMessage.info(`Deleted node ${nodeUuid}`);
  });
};

const createEdgeMutation = useCreateEdgeMutation();
const createEdge = async () => {
  if (selectedNodeUUIDs.value.length !== 2) {
    ElMessage.info("Creating a connection requires exactly 2 selected scenes.");
    return;
  }
  const [nodeInUuid, nodeOutUuid] = selectedNodeUUIDs.value;
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
