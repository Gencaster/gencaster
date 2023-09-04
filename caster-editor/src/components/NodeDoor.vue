<script setup lang="ts">
import { useDeleteNodeDoorMutation, type NodeDoor } from "@/graphql";
import { ElRow, ElCol, ElInput, ElIcon, ElMessage } from "element-plus";
import { Delete } from "@element-plus/icons-vue";
import { computed, ref, type Ref } from "vue";
import { storeToRefs } from "pinia";
import { useInterfaceStore } from "@/stores/InterfaceStore";

type NodeDoorPick = Pick<
  NodeDoor,
  "code" | "doorType" | "isDefault" | "name" | "order" | "uuid"
>;

const props = defineProps<{
  nodeDoor: NodeDoorPick;
}>();

const { newNodeDoorUpdates } = storeToRefs(useInterfaceStore());

const deleteNodeDoorMutation = useDeleteNodeDoorMutation();

const deleteNodeDoor = async () => {
  const { error, data } = await deleteNodeDoorMutation.executeMutation({
    nodeDoorUuid: props.nodeDoor.uuid,
  });
  if (error || !data?.deleteNodeDoor) {
    ElMessage.error(`Failed to delete node door`);
  }
};

const name: Ref<string> = ref(props.nodeDoor.name);
const nodeDoorName = computed<string>({
  get() {
    return name.value;
  },
  set(value) {
    console.log(`Name is now ${value}`);
    name.value = value;
    let update = newNodeDoorUpdates.value.get(props.nodeDoor.uuid);

    if (update) {
      update.name = name.value;
    } else {
      newNodeDoorUpdates.value.set(props.nodeDoor.uuid, {
        uuid: props.nodeDoor.uuid,
        name: name.value,
      });
    }
    return name.value;
  },
});

const code: Ref<string> = ref(props.nodeDoor.code);
const nodeDoorCode = computed<string>({
  get() {
    return code.value;
  },
  set(value) {
    code.value = value;
    let update = newNodeDoorUpdates.value.get(props.nodeDoor.uuid);

    if (update) {
      update.code = code.value;
    } else {
      newNodeDoorUpdates.value.set(props.nodeDoor.uuid, {
        uuid: props.nodeDoor.uuid,
        code: code.value,
      });
    }
    return code.value;
  },
});
</script>

<template>
  <div class="node-door radius">
    <ElRow :gutter="10">
      <ElCol :span="6">
        <span
          class="node-door-name"
          :class="{
            'default-door': nodeDoor.isDefault,
          }"
        >
          <ElInput
            v-model="nodeDoorName"
            :disabled="nodeDoor.isDefault"
          />
        </span>
      </ElCol>
      <ElCol :span="16">
        <ElInput v-model="nodeDoorCode" />
      </ElCol>
      <ElCol :span="2">
        <ElButton
          type="danger"
          :disabled="nodeDoor.isDefault"
          @click="deleteNodeDoor()"
        >
          <ElIcon><Delete /></ElIcon>
        </ElButton>
      </ElCol>
    </ElRow>
  </div>
</template>

<style scoped>
.node-door {
  border-radius: 4px;
  border: 1px solid var(--el-border-color);
}

.default-door {
  background-color: aquamarine;
}
</style>
