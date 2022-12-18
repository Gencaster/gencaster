<template>
  <div class="block">
    <!-- python -->
    <div v-if="editorType === CellType.Python" class="editor-python">
      <Codemirror
        v-model="codemirrorCode" placeholder="Code goes here..." :autofocus="false" :indent-with-tab="true"
        :tab-size="2" :extensions="extensions" @ready="codemirrorReady" @change="emitCodemirror('change', $event)"
        @focus="emitCodemirror('focus', $event)" @blur="emitCodemirror('blur', $event)"
      />
    </div>

    <!-- supercollider -->
    <div v-if="editorType === CellType.Supercollider" class="editor-supercollider">
      <Codemirror
        v-model="codemirrorCode" placeholder="Code goes here..." :autofocus="false" :indent-with-tab="true"
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
import type { Node as GraphNode } from "v-network-graph";
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
const graphStore: GraphNode = useGraphStore();

// Block Data
const graphNodeData: GraphNode = computed(() => {
  return graphStore.graphUserState.nodes[props.nodeUuid];
});

// Variables
const editorType = ref<string>(props.cellData.cellType);
const codemirrorCode = ref<string>();
const extensions = ref<any>([]);

// methods
const emitCodemirror = (eventType?: string, event?: any) => {
  if (eventType === "change") {
    // update prop in store
    // console.log(props.index);
    console.log(props.nodeUuid);
    console.log(typeof JSON.stringify(props.cellData.cellCode) === typeof JSON.stringify(event));
  }

  // setTimeout(() => {
  //   console.log("changed");
  //   console.log(props.cellData.cellCode);
  //   console.log(codemirrorCode.value);
  //   // console.log(codemirrorCode.value);
  //   console.log(typeof JSON.stringify(props.cellData.cellCode) === typeof JSON.stringify(codemirrorCode.value));
  // }, 100);
};
const codemirrorReady = () => { };

onMounted(() => {
  switch (editorType.value) {
    case CellType.Python:
      codemirrorCode.value = props.cellData.cellCode;
      extensions.value = [python()];
      break;

    case CellType.Supercollider:
      codemirrorCode.value = props.cellData.cellCode;
      extensions.value = [python()];
      break;

    default:
      break;
  }
});
</script>
