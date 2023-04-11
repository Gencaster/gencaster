<template>
  <div>
    <ElDialog
      v-model="showDialog"
      title="Careful"
      width="25%"
      center
      lock-scroll
      :show-close="false"
    >
      <span>
        Are you sure to delete Node "{{ node.name }}"?
      </span>
      <template #footer>
        <span class="dialog-footer">
          <ElButton
            text
            bg
            @click="emit('cancel')"
          >Cancel</ElButton>
          <ElButton
            color="#FF0000"
            @click="deleteNode()"
          >
            Delete Node
          </ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, type Ref } from 'vue';
import { type Node, useDeleteNodeMutation } from "@/graphql";

export type NodeDelete = Pick<Node, 'name' | 'uuid'>

const emit = defineEmits<{
    (e: 'deleted'): void,
    (e: 'cancel'): void
}>();

const props = defineProps<{
    node: NodeDelete
}>();

const showDialog: Ref<boolean> = ref(true);

const deleteNodeMutation = useDeleteNodeMutation();

const deleteNode = async () => {
    const { error } = await deleteNodeMutation.executeMutation({nodeUuid: props.node.uuid})
    if(error) {
        alert(`Failed to delete Node: ${error.message}`)
    } else {
        emit('deleted')
    }
}

</script>
