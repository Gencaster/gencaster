<template>
  <div class="block">
    <!-- python -->
    <div v-if="scriptCell?.cellType === CellType.Python" class="editor-python">
      <Codemirror
        v-model="scriptCell.cellCode"
        placeholder="Code goes here..."
        :autofocus="false"
        :indent-with-tab="true"
        :tab-size="2"
        :extensions="[python()]"
        @ready="() => { domReady = true }"
        @change="emitCodemirror('change', $event)"
        @focus="emitCodemirror('focus', $event)"
        @blur="emitCodemirror('blur', $event)"
      />
    </div>

    <!-- supercollider -->
    <div v-if="scriptCell?.cellType === CellType.Supercollider" class="editor-supercollider">
      <Codemirror
        v-model="scriptCell.cellCode"
        placeholder="Code goes here..."
        :autofocus="false"
        :indent-with-tab="true"
        :tab-size="2"
        :extensions="[python()]"
        @ready="() => { domReady = true }"
        @change="emitCodemirror('change', $event)"
        @focus="emitCodemirror('focus', $event)"
        @blur="emitCodemirror('blur', $event)"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
// code editor
import { Codemirror } from "vue-codemirror";
import { python } from "@codemirror/lang-python";
import type { Ref } from "vue";
import { storeToRefs } from "pinia";
import { CellType } from "@/graphql/graphql";
import type { GetNodeQuery, ScriptCell } from "@/graphql/graphql";
import { useNodeStore } from "~~/src/stores/NodeStore";
const props = defineProps<BlockProps>();

interface BlockProps {
  scriptCellUuid: String
  index: number
}

// Store
const { scriptCellsModified, node } = storeToRefs(useNodeStore());

// Variables
const scriptCell = ref<GetNodeQuery["node"]["scriptCells"][0] | undefined>(node.value.scriptCells.find((x) => { return x.uuid === props.scriptCellUuid; }));
const domReady: Ref<boolean> = ref(false);

const emitCodemirror = (eventType?: string, event?: any) => {
  if (!domReady.value)
    return;

  if (eventType === "change")
    scriptCellsModified.value = true;
};
</script>
