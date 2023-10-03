<script setup lang="ts">
import { PlaybackChoices, type Node, type AudioFile } from "@/graphql";
import { CellType, useCreateScriptCellsMutation } from "@/graphql";
import { useInterfaceStore } from "@/stores/InterfaceStore";
import { storeToRefs } from "pinia";
import { ref, type Ref } from "vue";
import DialogRenameNode from "./DialogRenameNode.vue";
import AudioFileBrowser from "./AudioFileBrowser.vue";
import { ElMessage } from "element-plus";
import DialogExitNode from "@/components/DialogExitNode.vue";

export type NodeName = Pick<Node, "name" | "uuid">;

const props = defineProps<{
  node: NodeName;
}>();

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const emit = defineEmits<{
  (e: "saveNode"): void;
}>();

const interfaceStore = useInterfaceStore();
const { showNodeEditor, unsavedNodeChanges, cachedNodeData } =
  storeToRefs(interfaceStore);

const showAudioFileBrowser: Ref<boolean> = ref(false);
const showNodeExitDialog: Ref<boolean> = ref(false);
const showRenameNodeDialog: Ref<boolean> = ref(false);

const createScriptCellMutation = useCreateScriptCellsMutation();

const closeScriptCellEditor = async () => {
  if (!unsavedNodeChanges.value) {
    showNodeEditor.value = false;
  } else {
    showNodeExitDialog.value = true;
  }
};

const addScriptCell = async (cellType: CellType) => {
  if (unsavedNodeChanges.value) {
    ElMessage.warning(
      "Please save your changes before adding a new script cell",
    );
    return;
  }
  if (cellType === CellType.Audio) {
    showAudioFileBrowser.value = true;
    return;
  }
  const { error } = await createScriptCellMutation.executeMutation({
    nodeUuid: props.node.uuid,
    scriptCellInputs: [
      {
        cellType: cellType,
        cellCode: "",
      },
    ],
  });
  if (error) {
    ElMessage.error(`Error on creating script cell: ${error.message}`);
  }
};

const createAudioCell = async (audioFile: Pick<AudioFile, "uuid">) => {
  const { error } = await createScriptCellMutation.executeMutation({
    nodeUuid: props.node.uuid,
    scriptCellInputs: [
      {
        audioCell: {
          audioFile: {
            uuid: audioFile.uuid,
          },
          playback: PlaybackChoices.AsyncPlayback,
        },
        cellCode: "",
        cellType: CellType.Audio,
      },
    ],
  });
  if (error) {
    alert(`Error on creating audio cell: ${error.message}`);
  }
  showAudioFileBrowser.value = false;
};
</script>

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
          :disabled="!unsavedNodeChanges"
          @click="interfaceStore.executeUpdates()"
        >
          Save Node
        </button>
        <button
          class="unstyled"
          @click="closeScriptCellEditor()"
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
    <DialogExitNode
      v-if="showNodeExitDialog"
      @save="
        () => {
          interfaceStore.executeUpdates();
          showNodeEditor = false;
          cachedNodeData = undefined;
        }
      "
      @no-save="
        () => {
          interfaceStore.resetUpdates();
          showNodeEditor = false;
          cachedNodeData = undefined;
        }
      "
      @cancel="
        () => {
          showNodeExitDialog = false;
        }
      "
    />
    <AudioFileBrowser
      v-if="showAudioFileBrowser"
      @cancel="showAudioFileBrowser = false"
      @selected-audio-file="(audioFile) => createAudioCell(audioFile)"
    />
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/scss/variables.module.scss";

.editor-header {
  display: block;
  position: fixed;
  width: 798px;
  z-index: 2;
  background-color: $mainWhite;

  .title {
    display: flex;
    height: $menuHeight;
    justify-content: space-between;
    align-items: center;
    margin-top: 5px;
    margin-bottom: 4px;

    padding-left: 15px;
    padding-right: 15px;

    .left {
      button {
        color: $grey-dark;

        &:hover {
          font-style: italic;
          background-color: transparent;
        }
      }
    }

    .right {
      transform: translateX(8px);
      text-decoration: underline;
    }

    .left,
    .right {
      display: flex;
      justify-content: center;
      align-items: center;

      p {
        margin: 0;
      }
    }
  }

  .node-menu-bar {
    display: flex;
    align-items: center;
    height: $menuHeight;
    background-color: transparent;
    border-bottom: 1px solid $grey;
    border-top: 1px solid $grey;
    padding-left: 15px;
    padding-right: 15px;

    button {
      border: 0;
      margin: 0;
      padding: 0;
      background-color: transparent;
      padding-left: 10px;
      padding-right: 10px;
      transform: translateX(-10px);

      border-radius: 2px;
      height: 24px;
      cursor: pointer;

      &:hover {
        background-color: $grey-light;
      }
    }
  }
}
</style>
