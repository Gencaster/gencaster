<script setup lang="ts">
import { DoorType, useCreateNodeDoorMutation } from "@/graphql";
import { ElMessage, ElDialog } from "element-plus";
import { ref, type Ref } from "vue";

const props = defineProps<{
  nodeUuid: string;
}>();

const emit = defineEmits<{
  (e: "closed"): void;
}>();

const newDoorName: Ref<string> = ref("");

const showDialog: Ref<boolean> = ref(true);

const createDoorMutation = useCreateNodeDoorMutation();

const createDoor = async () => {
  const { error } = await createDoorMutation.executeMutation({
    nodeUuid: props.nodeUuid,
    name: newDoorName.value,
    code: "",
    doorType: DoorType.Output,
    order: 10,
  });
  if (error) {
    ElMessage.error(`Could not create new node door: ${error.message}`);
  } else {
    emit("closed");
  }
};
</script>

<template>
  <div>
    <ElDialog
      v-model="showDialog"
      title="Create new node exit"
      align-center
      :show-close="true"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
    >
      <ElInput
        v-model="newDoorName"
        placeholder="New exit name"
      />
      <template #footer>
        <span class="dialog-footer">
          <ElButton
            type="danger"
            @click="() => emit('closed')"
          >Cancel</ElButton>
          <ElButton
            type="primary"
            :disabled="newDoorName.length < 1"
            @click="createDoor()"
          >
            Create
          </ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>
