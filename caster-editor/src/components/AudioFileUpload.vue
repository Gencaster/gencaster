<script lang="ts" setup>
import { ElButton, ElMessage, ElUpload, type UploadUserFile, ElInput, ElForm, ElFormItem, type FormRules, type FormInstance } from "element-plus";

import { reactive, ref, type Ref } from "vue";
import { useUploadAudioFileMutation, type AddAudioFile, type Scalars} from "@/graphql";

const fileList: Ref<UploadUserFile[]> = ref([]);

const audioFileUpload = useUploadAudioFileMutation();

const emit = defineEmits<{
  (e: 'uploadedNewFile', audioFileUUID: Scalars['UUID']): void
}>();

const form: {name: string | undefined, description: string | undefined} = reactive({
  name: undefined,
  description: undefined,
});

const formRef = ref<FormInstance>();

const rules = reactive<FormRules>({
  name: {required: true, message: 'Please insert a name', trigger: 'blur'},
  description: {required: false},
});

const submitUpload = async () => {
  if (!formRef.value) return;
  await formRef.value.validate((valid) => {
    if (valid) {
      doSubmit();
    } else {
      ElMessage.error("Input is missing");
    }
  });
};

const doSubmit = async() => {
  const audioUpload: AddAudioFile = {
    name: form.name ?? (Math.random() + 1).toString(36).substring(7),
    description: form.description ?? "",
    fileName: fileList.value[0].name,
    file: fileList.value[0].raw as File,
  };

  const { data, error } = await audioFileUpload.executeMutation({addAudioFile: audioUpload});
  if(error) {
    ElMessage.error("Unexpected error on uploading the audio: " + error.message);
  }
  if(data?.addAudioFile.__typename=="InvalidAudioFile") {
    ElMessage.error(`Uploaded invalid audio file: ${data.addAudioFile.error}`);
  } else if(data) {
    ElMessage.success(`Uploaded audio file successfully`);
    emit('uploadedNewFile', data.addAudioFile.uuid);
    form.description = undefined;
    form.name = undefined;
  }
};
</script>

<template>
  <div>
    <ElUpload
      ref="uploadRef"
      v-model:file-list="fileList"
      class="uploader"
      :auto-upload="false"
      :limit="1"
      accept=".wav,.flac"
      drag
    >
      <div class="el-upload__text">
        Drop file here or <em>click to upload</em>
      </div>

      <template #tip>
        <div class="el-upload__tip">
          wav/flac files
        </div>
      </template>
    </ElUpload>

    <ElForm
      ref="formRef"
      :model="form"
      :rules="rules"
      label-position="top"
    >
      <ElFormItem
        label="Name"
        prop="name"
      >
        <ElInput
          v-model="form.name"
          placeholder="Audio name..."
        />
      </ElFormItem>
      <ElFormItem
        label="Description"
        prop="description"
      >
        <ElInput
          v-model="form.description"
          type="textarea"
          placeholder="Description"
        />
      </ElFormItem>
      <ElButton
        class="ml-3"
        type="primary"
        style="margin-top: 10px;"
        @click="submitUpload()"
      >
        Upload
      </ElButton>
    </ElForm>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/scss/variables.module.scss';

.uploader {
  .el-upload__text {
    color: $black;
    em {
      text-decoration: underline;
      color: $black;
    }
  }
}

</style>
