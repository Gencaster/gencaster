<script setup lang="ts">
import { type AudioFile, useUpdateAudioFileMutation } from "@/graphql";
import { ElMessage, ElForm, ElFormItem } from "element-plus";
import { ref, type Ref } from "vue";

export type AudioFileRename = Pick<AudioFile, "uuid" | "name" | "description">;

const emit = defineEmits<{
  (e: "updated"): void;
  (e: "cancel"): void;
}>();

const props = defineProps<{
  audioFile: AudioFileRename;
}>();

const showDialog: Ref<boolean> = ref(true);
const newName: Ref<string> = ref(props.audioFile.name);
const newDescription: Ref<string> = ref(props.audioFile.description);

const updateAudioFileMutation = useUpdateAudioFileMutation();

const update = async () => {
  const { error } = await updateAudioFileMutation.executeMutation({
    uuid: props.audioFile.uuid,
    updateAudioFile: {
      description: newDescription.value,
      name: newName.value,
    },
  });
  if (error) {
    ElMessage.error(`Could not rename audio file: ${error.message}`);
    return;
  }
  emit("updated");
};
</script>

<template>
  <div class="update-audio-file-dialog">
    <ElDialog
      v-model="showDialog"
      title="Update Audio file"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      align-center
    >
      <ElForm label-width="120px">
        <ElFormItem label="Name">
          <ElInput
            v-model="newName"
            placeholder="Name"
          />
        </ElFormItem>
        <ElFormItem label="Description">
          <ElInput
            v-model="newDescription"
            placeholder="Description"
          />
        </ElFormItem>
      </ElForm>
      <template #footer>
        <span class="dialog-footer">
          <ElButton
            type="danger"
            @click="emit('cancel')"
          >Cancel</ElButton>
          <ElButton
            type="primary"
            @click="update()"
          > Confirm </ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>
