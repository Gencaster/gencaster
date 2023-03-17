<script lang="ts" setup>
import { computed } from "vue";
import FileUpload from "./FileUpload.vue";
import MediaPlayer from "./MediaPlayer.vue"
import type { AudioCell } from "@/graphql";
import { CellType, useAudioFilesQuery, PlaybackChoices  } from "@/graphql";
import { storeToRefs } from "pinia";
import { useNodeStore } from "@/stores/NodeStore";
import { useInterfaceStore } from "@/stores/InterfaceStore";

const nodeStore = useNodeStore();
const { node, } = storeToRefs(nodeStore);
const interfaceStore = useInterfaceStore();
const { showAudioSelector } = storeToRefs(interfaceStore);

// import { storeToRefs } from "pinia";

// Store
// import { useGraphStore } from "@/stores/GraphStore";

// import { useQuery } from '@urql/vue';

const audioFilesQuery = useAudioFilesQuery();

const { data: audioFiles, executeQuery: refreshData } = audioFilesQuery.executeQuery();

const filteredAudio = computed(() => {
  return audioFiles.value?.audioFiles
})

const selectAudio = (uuid: string) => {
  if (node.value === undefined) {
    console.log("You can not add a script cell if not selected properly");
    return;
  }

  nodeStore.createScriptCell({
    nodeUuid: node.value.node.uuid,
    newScriptCell: {
      // add cell as last cell by searching for highest current cell order
      cellOrder:
        node.value.node.scriptCells.length > 0
          ? Math.max(
            ...node.value.node.scriptCells.map((x) => {
              return x.cellOrder;
            })
          ) + 1
          : 0,
      cellCode: "",
      cellType: CellType.Audio,
      audioCell: {
        audioFile: {
          uuid: uuid,
        },
        playbackType: PlaybackChoices.AsyncPlayback,
      },
    },
  });

  showAudioSelector.value = false
  console.log("Added Audio");
  console.log(uuid)
}

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
        </div>
      </div>
      <div class="content">
        <div class="left">
          <FileUpload class="upload" />
        </div>
        <div class="right">
          <div class="list-wrapper">
            <div
              v-for="(audio, index) in filteredAudio"
              :key="index"
              class="row"
            >
              <MediaPlayer :audio="audio" />
              <button @click="selectAudio(audio.uuid)">
                <p>Select</p>
              </button>
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
