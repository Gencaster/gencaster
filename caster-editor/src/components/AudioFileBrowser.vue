<script lang="ts" setup>import { computed, ref, type Ref } from "vue";
import FileUpload from "./AudioFileUpload.vue";
import MediaPlayer, {type AudioType} from "./AudioFilePlayer.vue"
import { useAudioFilesQuery, type Scalars  } from "@/graphql";

const props = defineProps<{
  audioFileUUID?: {type: Scalars['UUID'], required: false}
}>();

const emit = defineEmits<{
  (e: 'selectedAudioFile', uuid: Scalars['UUID']): void
  (e: 'cancel'): void
}>();

const audioNameFilter: Ref<string> = ref("");
const { data, executeQuery: refreshData } = useAudioFilesQuery({variables: {audioNameFilter}}).executeQuery();

const selectedUUID = computed<Scalars["UUID"] | undefined>({
  get() {
    return props.audioFileUUID
  },
  set(value) {
    emit('selectedAudioFile', value);
    return value;
  }
});

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const doRefresh = () => {
  refreshData();
};

</script>

<template>
  <div class="audio-selector-wrapper">
    <div class="audio-selector-inner">
      <div class="header">
        <div class="left">
          <p>Upload Audio</p>
        </div>
        <div class="right">
          <p>Files</p>
          <ElInput
            v-model="audioNameFilter"
            placeholder="Search"
          />
        </div>
      </div>
      <div class="content">
        <div class="left">
          <FileUpload class="upload" />
          <el-button
            @click="emit('cancel')"
          >
            Cancel
          </el-button>
        </div>
        <div class="right">
          <div class="list-wrapper">
            <div
              v-if="data?.audioFiles"
            >
              <div
                v-for="(audioFile, index) in data?.audioFiles"
                :key="index"
                class="row"
              >
                <MediaPlayer
                  :audio-file="audioFile as AudioType"
                />
                <button @click="selectedUUID = audioFile.uuid">
                  <p>Select</p>
                </button>
              </div>
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
  width: 50%;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 999;
  background-color: rgba($white, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;

  .audio-selector-inner {
    width: 100%;
    height: 100%;
    max-width: 1200px;
    max-height: 520px;
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
    flex: 1;
    border-right: 1px solid $black;
  }

  .right {
    flex: 2;
  }

  .content {
    display: flex;
    height: calc(100% - 45px);

    .left,
    .right {
      padding-top: $spacingM;
      padding-bottom: $spacingM;
      height: 100%;
    }
    .list-wrapper {
      width: 100%;

      .row {
        width: 100%;
        display: flex;
        padding-top: 4px;
        padding-bottom: 4px;


        &:hover {
          background-color: $grey-light;
        }


        button {
          all: unset;
          cursor: pointer;
          width: auto;
          height: 26px;
          background: $green-light;
          border-radius: 4px;

          display: flex;
          align-items: center;
          justify-content: center;
          padding-left: 8px;
          padding-right: 8px;
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