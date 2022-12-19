<template>
  <div class="block">
    <!-- python -->
    <div v-if="editorType === CellType.Python" class="editor-python">
      <Codemirror
        v-model="code" placeholder="Code goes here..." :autofocus="false" :indent-with-tab="true"
        :tab-size="2" :extensions="extensions" @ready="codemirrorReady" @change="emitCodemirror('change', $event)"
        @focus="emitCodemirror('focus', $event)" @blur="emitCodemirror('blur', $event)"
      />
    </div>

    <!-- supercollider -->
    <div v-if="editorType === CellType.Supercollider" class="editor-supercollider">
      <Codemirror
        v-model="code" placeholder="Code goes here..." :autofocus="false" :indent-with-tab="true"
        :tab-size="2" :extensions="extensions" @ready="codemirrorReady" @change="emitCodemirror('change', $event)"
        @focus="emitCodemirror('focus', $event)" @blur="emitCodemirror('blur', $event)"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
// code editor
import { Codemirror } from "vue-codemirror";
import { python } from "@codemirror/lang-python";
import { useGraphStore } from "@/stores/GraphStore";
import { CellType } from "@/graphql/graphql";
import type { ScriptCell } from "@/graphql/graphql";
const props = defineProps<BlockProps>();

interface BlockProps {
  cellData: ScriptCell
  nodeUuid: string
  index: number
}

// Store
const graphStore = useGraphStore();

// Variables
const editorType = ref<string>(props.cellData.cellType);
const code = ref<string>(props.cellData.cellCode);
const extensions = ref<any>([]);
const domReady = ref<boolean>(false);

// methods
const codemirrorReady = () => {
  domReady.value = true;
};

const emitCodemirror = (eventType?: string, event?: any) => {
  if (!domReady.value)
    return;

  if (eventType === "change") {
    // this is the original unmuted
    // const original = props.cellData.cellCode;

    // this is the new code
    const newCode = event;

    // mutate store local
    graphStore.updateNodeScriptCellLocal(props.nodeUuid, newCode, props.cellData.cellOrder, props.cellData.cellType, props.cellData.uuid);
  }
};

onMounted(() => {
  switch (editorType.value) {
    case CellType.Python:
      extensions.value = [python()];
      break;

    case CellType.Supercollider:
      extensions.value = [python()];
      break;

    default:
      break;
  }
});
</script>
