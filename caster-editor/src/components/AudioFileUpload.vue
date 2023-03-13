<script lang="ts" setup>
import { ElUpload, type UploadUserFile } from "element-plus";

import { ref, type Ref } from "vue";
import { useUploadAudioFileMutation, type AddAudioFile } from "@/graphql";

const fileList: Ref<UploadUserFile[]> = ref([]);

const audioFileUpload = useUploadAudioFileMutation();
const errorMessage: Ref<string | undefined> = ref(undefined);

const submitUpload = async () => {
  if((fileList.value.length < 1)) {
    errorMessage.value = "No files selected for upload";
    return;
  }
  const audioUpload: AddAudioFile = {
    description: "Some fake description",
    fileName: fileList.value[0].name,
    file: fileList.value[0].raw as File
  };

  const { data, error } = await audioFileUpload.executeMutation({addAudioFile: audioUpload});
  if(error) {
    console.log("Unexpected error on uploading the audio: " + error.message);
  }
  if(data?.addAudioFile.__typename=="InvalidAudioFile") {
    errorMessage.value = data.addAudioFile.error;
  }
};

const limit = 1;
</script>

<template>
  <div>
    <ElUpload
      ref="uploadRef"
      v-model:file-list="fileList"
      class="upload-demo"
      :auto-upload="false"
      :limit="limit"
      accept=".wav,.flac"
    >
      <template #trigger>
        <el-button type="primary">
          select file
        </el-button>
      </template>

      <el-button
        class="ml-3"
        type="success"
        @click="submitUpload"
      >
        upload to server
      </el-button>

      <template #tip>
        <div class="el-upload__tip">
          wav/flac files
        </div>
      </template>
    </ElUpload>
    {{ errorMessage }}
  </div>
</template>
