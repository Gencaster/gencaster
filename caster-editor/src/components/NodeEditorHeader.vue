<template>
  <div class="editor-header">
    <div class="title">
      <div class="left">
        <p>{{ node.name }}</p>
        <button
          class="unstyled"
          @click="showRenameNodeDialog = true"
        >
          edit
        </button>
      </div>
      <div class="right">
        <button
          class="unstyled"
          @click="$emit('saveNode')"
        >
          Save Scene
        </button>
        <button
          class="unstyled"
          @click="showNodeEditor = false"
        >
          Close
        </button>
      </div>
    </div>
    <div class="node-menu-bar">
      <button @click="addScriptCell(CellType.Markdown)">
        + Markdown
      </button>
      <button @click="addScriptCell(CellType.Audio)">
        + Audio
      </button>
      <button @click="addScriptCell(CellType.Python)">
        + Python
      </button>
      <button @click="addScriptCell(CellType.Supercollider)">
        + Supercollider
      </button>
      <button @click="addScriptCell(CellType.Comment)">
        + Comment
      </button>
    </div>
    <DialogRenameNode
      v-if="showRenameNodeDialog"
      :node="node"
      @cancel="showRenameNodeDialog = false"
      @renamed="showRenameNodeDialog = false"
    />
    <AudioFileBrowser
      v-if="showAudioFileBrowser"
      @cancel="showAudioFileBrowser = false"
      @selected-audio-file="(uuid) => createAudioCell(uuid)"
    />
  </div>
</template>

<script setup lang="ts">
import { PlaybackChoices, type Node, type Scalars } from '@/graphql';
import { CellType, useCreateUpdateScriptCellsMutation } from "@/graphql";
import { useInterfaceStore } from '@/stores/InterfaceStore';
import { storeToRefs } from 'pinia';
import { ref, type Ref } from 'vue';
import DialogRenameNode from './DialogRenameNode.vue';
import AudioFileBrowser from './AudioFileBrowser.vue';

export type NodeName = Pick<Node, 'name' | 'uuid'>

const props = defineProps<{
    node: NodeName
}>();

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const emit = defineEmits<{
  (e: 'saveNode'): void
}>();

const { showNodeEditor } = storeToRefs(useInterfaceStore());

const showAudioFileBrowser: Ref<boolean> = ref(false);

const showRenameNodeDialog: Ref<boolean> = ref(false);

const createScriptCellMutation = useCreateUpdateScriptCellsMutation();

const addScriptCell = async (cellType: CellType) => {
    console.log("Add something");
    if(cellType===CellType.Audio) {
      showAudioFileBrowser.value = true;
      return;
    }
    const {error} = await createScriptCellMutation.executeMutation({
      nodeUuid: props.node.uuid,
      scriptCellInputs: [{
        cellType: cellType,
        cellCode: '',
      }]
    });
    if(error) {
      alert(`Error on creating script cell: ${error.message}`);
    }
}

const createAudioCell = async (audioFileUUID: Scalars['UUID']) => {
  const { error } = await createScriptCellMutation.executeMutation({
    nodeUuid: props.node.uuid,
    scriptCellInputs: [{
      audioCell: {
        audioFile: {
          uuid: audioFileUUID
        },
        playback: PlaybackChoices.AsyncPlayback,
      },
      cellCode: '',
      cellType: CellType.Audio,
    }]
  });
  if(error) {
    alert(`Error on creating audio cell: ${error.message}`)
  }
  showAudioFileBrowser.value = false;
}

</script>
