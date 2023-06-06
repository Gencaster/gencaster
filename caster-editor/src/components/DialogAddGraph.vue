<template>
  <div>
    <ElDialog
      v-model="showDialog"
      title="Create graph"
      :show-close="false"
    >
      <ElInput
        id="graphNameInput"
        v-model="newGraphDialogName"
        placeholder="Name of graph"
      />
      <template #footer>
        <span class="dialog-footer">
          <ElButton @click="() => emit('aborted')">Cancel</ElButton>
          <ElButton
            color="#ADFF00"
            type="primary"
            @click="createGraph()"
          >
            Confirm
          </ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>

<script setup lang="ts">

import { ref, type Ref } from "vue";
import {useCreateGraphMutation} from "@/graphql";

const emit = defineEmits<{
    (e: 'aborted'): void,
    (e: 'created'): void,
}>();

const newGraphDialogName: Ref<string> = ref("");
const showDialog: Ref<boolean> = ref(true);
const createGraphMutation = useCreateGraphMutation();

// from https://www.30secondsofcode.org/js/s/slugify/
const slugify = (str: string): string => {
  return str
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '-')
    .replace(/[\s_-]+/g, '-')
    .replace(/^-+|-+$/g, '-');
};

const createGraph = async() => {
  const { error: createGraphError } = await createGraphMutation.executeMutation({graphInput: {
    name: newGraphDialogName.value,
    displayName: newGraphDialogName.value,
    slugName: slugify(newGraphDialogName.value),
    publicVisible: true,
  }});

  if(createGraphError) {
    alert("Could not create graph: " + createGraphError.message);
    return;
  }
  newGraphDialogName.value = "";
  emit('created');
};
</script>
