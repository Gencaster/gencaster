<script lang="ts" setup>
import { computed, ref, type Ref } from "vue";
import AudioFileUpload from "./AudioFileUpload.vue";
import MediaPlayer from "./AudioFilePlayer.vue";
import DialogUpdateAudioFile from "@/components/DialogUpdateAudioFile.vue";
import { useAudioFilesQuery, type AudioFile, type DjangoFileType, type AudioFilesQuery } from "@/graphql";
import { ElButton, ElTable, ElTableColumn } from "element-plus";

export type AudioFilePicker = Pick<AudioFile, 'name' | 'uuid'> & {file?: Pick<DjangoFileType, 'url'> | undefined | null};

const emit = defineEmits<{
  (e: 'selectedAudioFile', audioFile: AudioFilesQuery['audioFiles'][0]): void
  (e: 'cancel'): void
}>();

const audioNameFilter: Ref<string> = ref("");
const showUpdateAudioFileDialog: Ref<boolean> = ref(false);
const selectedAudioFile: Ref<AudioFile | undefined> = ref(undefined);

const { data, executeQuery, fetching } = useAudioFilesQuery({ variables: {
  audioNameFilter,
} });

const tableData = computed(() => {
  if(!data.value) {
    return [];
  };
  return data.value.audioFiles.map((x) => {
    return {
      ...x,
      'createdDate': new Date(x.createdDate).toISOString().slice(0, 10),
    };
  });
});

// const updated = () => {
//   showUpdateAudioFileDialog.value = false;
//   executeQuery();
// };
</script>

<template>
  <div class="audio-selector-wrapper">
    <div class="audio-selector-inner">
      <div class="header">
        <div class="left">
          <p>Upload Audio</p>
        </div>
        <div class="right">
          <ElInput
            v-model="audioNameFilter"
            placeholder="Search"
          />
          <ElButton
            type="info"
            @click="emit('cancel')"
          >
            Cancel
          </ElButton>
        </div>
      </div>
      <div class="update-dialog">
        <DialogUpdateAudioFile
          v-if="showUpdateAudioFileDialog && selectedAudioFile"
          :audio-file="selectedAudioFile"
          @cancel="showUpdateAudioFileDialog = false"
          @updated="showUpdateAudioFileDialog = false && executeQuery()"
        />
      </div>
      <div class="content">
        <div class="left">
          <AudioFileUpload
            class="upload"
            @uploaded-new-file="executeQuery()"
          />
        </div>
        <div class="right">
          <div
            v-loading="fetching"
            class="list-wrapper"
          >
            <div v-if="data?.audioFiles">
              <ElTable
                :data="tableData"
                :fit="true"
              >
                <ElTableColumn
                  prop="name"
                  label="Name"
                />
                <ElTableColumn
                  prop="description"
                  label="Description"
                />
                <ElTableColumn
                  prop="createdDate"
                  label="Created"
                />
                <ElTableColumn
                  fixed="right"
                  label="Operations"
                  class-name="operations-column"
                >
                  <template #default="scope">
                    <MediaPlayer
                      type="browser"
                      :audio-file="scope.row"
                    />
                    <ElButton
                      type="info"
                      size="small"
                      @click="() => {
                        selectedAudioFile = scope.row,
                        showUpdateAudioFileDialog = true;
                      }"
                    >
                      Edit
                    </ElButton>
                    <ElButton
                      type="primary"
                      size="small"
                      @click="emit('selectedAudioFile', scope.row)"
                    >
                      Choose
                    </ElButton>
                  </template>
                </ElTableColumn>
              </ElTable>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/scss/variables.module.scss';

.audio-selector-wrapper {
  width: 100%;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 999;
  background-color: rgba($white, 0.8);
  display: flex;
  justify-content: center;
  align-items: flex-start;
  margin: 0;
  padding: 0;

  .audio-selector-inner {
    width: calc(100% - $menuHeight);
    height: calc(100vh - 100px);
    margin-top: calc(2.5 * $menuHeight);
    border: 1px solid $black;
    background-color: $white;
  }

  .header {
    display: flex;
    height: 45px;
    border-bottom: 1px solid $black;

    .left,
    .right {
      align-items: center;
    }

    .right {
      gap: $spacingM;
    }
  }

  .left,
  .right {
    padding-left: $spacingM;
    padding-right: $spacingM;
    height: 100%;
    display: flex;

    p {
      margin: 0;
    }
  }

  .left {
    width: calc(100%/3);
    border-right: 1px solid $black;
  }

  .right {
    width: calc(100%/3*2);
  }

  .content {
    display: flex;
    height: calc(100% - 45px);

    .left,
    .right {
      padding-top: $spacingM;
      padding-bottom: $spacingM;
      height: 100%;
      flex-shrink: 0;
    }

    .list-wrapper {
      width: 100%;
      overflow-y: scroll;

      :deep(.operations-column) {
       display: flex;
        .cell {
          display: flex;
        }
      }
    }

    .upload {
      width: 100%;
      height: 100%;
    }
  }
}
</style>
