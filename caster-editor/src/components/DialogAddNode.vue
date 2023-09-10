<script setup lang="ts">
import { useCreateNodeMutation } from "@/graphql";
import { useInterfaceStore } from "@/stores/InterfaceStore";
import { ElMessage, ElDialog } from "element-plus";
import { storeToRefs } from "pinia";
import { computed, ref, type Ref } from "vue";
import variables from "@/assets/scss/variables.module.scss";

const props = defineProps<{
  graphUuid: string;
}>();

const emit = defineEmits<{
  (e: "closed"): void;
}>();

const { vueFlowRef } = storeToRefs(useInterfaceStore());

const newNodeName: Ref<string> = ref("");

const hasName = computed(() => newNodeName.value.length > 0);

const showDialog: Ref<boolean> = ref(true);

const createNodeMutation = useCreateNodeMutation();

const createNode = async () => {
  let positionX = 0;
  let positionY = 0;
  if (vueFlowRef.value) {
    const { height, width } = vueFlowRef.value.dimensions;
    const currentTransform = vueFlowRef.value.getTransform();

    positionX =
      width / 2 - currentTransform.x - parseInt(variables.nodeDefaultWidth) / 2;
    positionY = (height / 2 - currentTransform.y) * 0.9;
  }

  console.log("Props are", props.graphUuid);

  const { error } = await createNodeMutation.executeMutation({
    name: newNodeName.value,
    color: "primary",
    positionX,
    positionY,
    graphUuid: props.graphUuid,
  });
  if (error) {
    ElMessage.error(`Could not create node: ${error.message}`);
  }
  emit("closed");
};
</script>

<template>
  <div>
    <ElDialog
      v-model="showDialog"
      title="Create new node"
      align-center
      :show-close="true"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
    >
      <ElInput
        id="graphNameInput"
        v-model="newNodeName"
        placeholder="New node name"
      />
      <template #footer>
        <span class="dialog-footer">
          <ElButton
            type="danger"
            @click="() => emit('closed')"
          >Cancel</ElButton>
          <ElButton
            type="primary"
            :disabled="!hasName"
            @click="createNode()"
          >
            Create
          </ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>
