<script lang="ts" setup>
import AudioFileUpload from "./AudioFileUpload.vue";
// import { storeToRefs } from "pinia";

// Store
// import { useGraphStore } from "@/stores/GraphStore";

import { useAudioFilesQuery } from "@/graphql";
// import { useQuery } from '@urql/vue';

const audioFilesQuery = useAudioFilesQuery();

const { data: audioFiles, executeQuery: refreshData } = audioFilesQuery.executeQuery();

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
          <!-- <p>{{ graphInStore }}</p> -->
        </div>
      </div>
      <div class="content">
        <div class="left">
          <AudioFileUpload />
        </div>
        <div class="right">
          <div class="list-wrapper">
            <button @click="doRefresh()">
              refresh
            </button>
            {{ audioFiles }}
            <!-- <div
              v-for="(audio, index) in placeholderAudioList"
              :key="index"
            >
              <p>{{ audio.name }}</p>
            </div> -->
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
    }
  }
}
</style>
