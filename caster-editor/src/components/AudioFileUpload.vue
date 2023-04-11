<script lang="ts" setup>
import { ElButton, ElUpload, type UploadUserFile } from "element-plus";

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
    name: (Math.random() + 1).toString(36).substring(7),
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
      class="uploader"
      :auto-upload="false"
      :limit="limit"
      accept=".wav,.flac"
      drag
    >
      <!-- <template #trigger>
        <ElButton>
          select file
        </ElButton>
      </template> -->

      <div class="el-upload__text">
        Drop file here or <em>click to upload</em>
      </div>

      <template #tip>
        <div class="el-upload__tip">
          wav/flac files
        </div>
      </template>
    </ElUpload>
    {{ errorMessage }}

    <ElButton
      class="ml-3"
      type="success"
      @click="submitUpload()"
    >
      upload to server
    </ElButton>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/scss/variables.module.scss';

.uploader {

}

</style>
