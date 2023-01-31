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
        :disable="dragging"
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
        :disable="dragging"
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
import type { NodeSubscription, ScriptCell } from "@/graphql/graphql";
import { useNuxtApp } from "#app";

const props = defineProps<BlockProps>();
interface BlockProps {
  scriptCellUuid: String
  index: number
  dragging: boolean
}

const nuxtApp = useNuxtApp();

// Store
const nodeStore = nuxtApp.nodeStore;
const { scriptCellsModified, node } = storeToRefs(nodeStore);

// Variables
const scriptCell = ref<NodeSubscription["node"]["scriptCells"][0] | undefined>(node.value?.node.scriptCells.find((x: ScriptCell) => { return x.uuid === props.scriptCellUuid; }));
const domReady: Ref<boolean> = ref(false);
const originalValue = ref<string>("");

const emitCodemirror = (eventType?: string, event?: any) => {
  if (!domReady.value)
    return;

  if (eventType === "change")
    scriptCellsModified.value = true;
};

onMounted(() => {
  if (scriptCell.value)
    originalValue.value = scriptCell.value.cellCode;
});
</script>
