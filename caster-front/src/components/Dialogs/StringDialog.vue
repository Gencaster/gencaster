<script setup lang="ts">
import { ElInput } from "element-plus";
import { type Ref, ref } from "vue";
import type { UserDataRequest } from "@/models";
import { type Scalars, useSendStreamVariableMutation } from "@/graphql";

const props = defineProps<{
  request: UserDataRequest
  streamUuid: Scalars["UUID"]
}>();

const emit = defineEmits<{
  (e: "submitted"): void
}>();

const userInput: Ref<string> = ref("");

const streamVariableMutation = useSendStreamVariableMutation();
const dialogVisible: Ref<boolean> = ref(true);

const execute = async () => {
  await streamVariableMutation.executeMutation({
    streamVariables: [{
      streamUuid: props.streamUuid,
      streamToSc: false,
      key: props.request.key,
      value: userInput.value
    }]
  });
  emit("submitted");
  dialogVisible.value = false;
};
</script>

<template>
  <div>
    <ElDialog
      v-model="dialogVisible"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <p class="description">
        {{ request.description }}
      </p>
      <div class="data">
        <div class="component string-component">
          <ElInput
            v-model="userInput"
            :placeholder="request.placeholder"
          />
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <div class="confirm">
            <ElButton class="caps green" size="default" type="default" @click="execute()">
              Ok
            </ElButton>
          </div>
        </span>
      </template>
    </ElDialog>
  </div>
</template>
