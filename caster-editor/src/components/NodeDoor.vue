<script setup lang="ts">
import { useDeleteNodeDoorMutation, type NodeDoor } from "@/graphql";
import { ElRow, ElCol, ElInput, ElMessage } from "element-plus";
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
  <div class="node-door">
    <ElRow
      :gutter="10"
      class="input"
    >
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
      <ElCol :span="18">
        <ElInput
          v-if="nodeDoor.isDefault"
          v-model="nodeDoorCode"
          autosize
          type="textarea"
          placeholder="Default"
          disabled
        />
        <ElInput
          v-else
          v-model="nodeDoorCode"
          autosize
          type="textarea"
          placeholder="Please input"
        />
      </ElCol>
    </ElRow>
    <button
      class="unstyled"
      :disabled="nodeDoor.isDefault"
      @click="deleteNodeDoor()"
    >
      <div class="icon">
        <Delete />
      </div>
    </button>
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/scss/variables.module.scss";

.node-door {
  margin-bottom: 12px;
  display: flex;
  width: 100%;
  justify-content: space-between;

  .input {
    width: calc(100% - 25px);
  }

  button {
    border: none;
    background-color: transparent;
    width: 31px;
    height: 31px;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: $borderRadius;
    transform: translateX(5px);
    .icon {
      width: 20px;
      height: 20px;
    }

    &:disabled {
      opacity: 0.4;
    }

    &:disabled:hover {
      background-color: transparent;
    }

    &:hover:not([disabled]) {
      background-color: $grey-light;
    }
  }
}
</style>
