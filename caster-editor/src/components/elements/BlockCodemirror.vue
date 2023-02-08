<template>
  <div class="block">
    <!-- python -->
    <div
      v-if="scriptCell?.cellType === CellType.Python"
      class="editor-python"
    >
      <Codemirror
        v-model="scriptCell.cellCode"
        placeholder="Code goes here..."
        :autofocus="false"
        :indent-with-tab="true"
        :tab-size="2"
        :extensions="[python()]"
        :disable="dragging"
        @ready="
          () => {
            domReady = true;
          }
        "
        @change="emitCodemirror('change')"
        @focus="emitCodemirror('focus')"
        @blur="emitCodemirror('blur')"
      />
    </div>

    <!-- supercollider -->
    <div
      v-if="scriptCell?.cellType === CellType.Supercollider"
      class="editor-supercollider"
    >
      <Codemirror
        v-model="scriptCell.cellCode"
        placeholder="Code goes here..."
        :autofocus="false"
        :indent-with-tab="true"
        :tab-size="2"
        :extensions="[python()]"
        :disable="dragging"
        @ready="
          () => {
            domReady = true;
          }
        "
        @change="emitCodemirror('change')"
        @focus="emitCodemirror('focus')"
        @blur="emitCodemirror('blur')"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
// code editor
export interface BlockProps {
  scriptCellUuid: String;
  index: number;
  dragging: boolean;
}

import { Codemirror } from "vue-codemirror";
import { python } from "@codemirror/lang-python";
import { ref } from "vue";
import type { Ref } from "vue";
import { storeToRefs } from "pinia";
import { CellType } from "@/graphql";
import type { NodeSubscription } from "@/graphql";
import { useNodeStore } from "@/stores/NodeStore";

const props = defineProps<BlockProps>();

// Store
const nodeStore = useNodeStore();
const { scriptCellsModified, node } = storeToRefs(nodeStore);

// Variables
const scriptCell = ref<NodeSubscription["node"]["scriptCells"][0] | undefined>(
  node.value?.node.scriptCells.find((x) => {
    return x.uuid === props.scriptCellUuid;
  })
);
const domReady: Ref<boolean> = ref(false);

const emitCodemirror = (eventType?: string) => {
  if (!domReady.value) return;

  if (eventType === "change") scriptCellsModified.value = true;
};
</script>
