<script setup lang="ts">
import { ref, type Ref } from "vue";
import { useRouter } from "vue-router";
import {
  useCreateGraphMutation,
  StreamAssignmentPolicy,
  GraphDetailTemplate,
} from "@/graphql";

const emit = defineEmits<{
  (e: "aborted"): void;
  (e: "created"): void;
}>();

const router = useRouter();
const newGraphDialogName: Ref<string> = ref("");
const showDialog: Ref<boolean> = ref(true);
const createGraphMutation = useCreateGraphMutation();

// from https://www.30secondsofcode.org/js/s/slugify/
const slugify = (str: string): string => {
  return str
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, "-")
    .replace(/[\s_-]+/g, "-")
    .replace(/^-+|-+$/g, "-");
};

const createGraph = async () => {
  const { error: createGraphError, data } =
    await createGraphMutation.executeMutation({
      graphInput: {
        name: newGraphDialogName.value,
        displayName: newGraphDialogName.value,
        slugName: slugify(newGraphDialogName.value),
        publicVisible: true,
        streamAssignmentPolicy: StreamAssignmentPolicy.OneUserOneStream,
        templateName: GraphDetailTemplate.Default,
      },
    });

  if (createGraphError) {
    alert("Could not create graph: " + createGraphError.message);
    return;
  }

  // route to graph
  router.push({ name: "graph", params: { uuid: data?.addGraph.uuid } });

  newGraphDialogName.value = "";
  emit("created");
};
</script>

<template>
  <div>
    <ElDialog
      v-model="showDialog"
      title="Create graph"
      :show-close="false"
      align-center
    >
      <ElInput
        id="graphNameInput"
        v-model="newGraphDialogName"
        placeholder="Name of graph"
      />
      <template #footer>
        <span class="dialog-footer">
          <ElButton
            type="danger"
            @click="() => emit('aborted')"
          >Cancel</ElButton>
          <ElButton
            type="primary"
            @click="createGraph()"
          > Confirm </ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>
