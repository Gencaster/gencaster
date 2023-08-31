<template>
  <div class="rename-node-dialog">
    <ElDialog
      v-model="showDialog"
      title="Rename Node"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      align-center
    >
      <ElInput
        v-model="newName"
        placeholder="Please input"
      />
      <template #footer>
        <span class="dialog-footer">
          <ElButton
            type="danger"
            @click="emit('cancel')"
          >Cancel</ElButton>
          <ElButton
            type="primary"
            @click="renameNode()"
          > Confirm </ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>

<script setup lang="ts">
import { type Node, useUpdateNodeMutation } from "@/graphql";
import { ref, type Ref } from "vue";

export type NodeRename = Pick<Node, "uuid" | "name">;

const emit = defineEmits<{
  (e: "renamed"): void;
  (e: "cancel"): void;
}>();

const props = defineProps<{
  node: NodeRename;
}>();

const showDialog: Ref<boolean> = ref(true);
const newName: Ref<string> = ref(props.node.name);

const udpateNodeMutation = useUpdateNodeMutation();

const renameNode = async () => {
  const { error } = await udpateNodeMutation.executeMutation({
    name: newName.value,
    nodeUuid: props.node.uuid,
  });
  if (error) {
    alert(`Could not rename node: ${error.message}`);
    return;
  }
  emit("renamed");
};
</script>
