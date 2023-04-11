<template>
  <div class="test-component node-editor">
    <NodeEditorHeader
      :node="node"
      @save-node="emit('saveNode')"
    />
    <div class="editor-header-spacer" />
    <NodeEditorCells
      v-model:script-cells="scriptCells"
    />
  </div>
</template>

<script setup lang="ts">
import NodeEditorHeader from "@/components/NodeEditorHeader.vue";
import NodeEditorCells from "./NodeEditorCells.vue";
import type { NodeSubscription } from '@/graphql';
import { computed } from "vue";

const props = defineProps<{
    node: NodeSubscription['node']
}>();

const emit = defineEmits<{
  (e: 'update:node', node: NodeSubscription['node']): void,
  (e: 'saveNode'): void
}>();

const scriptCells = computed({
  get() {
    return props.node.scriptCells;
  },
  set(value) {
    let nodeUpdate = {...props.node};
    nodeUpdate.scriptCells = value;
    emit('update:node', nodeUpdate);
    return value;
  }
});

</script>

<style scoped lang="scss">
.node-editor {
  z-index: 2;
  background-color: white;
  position: fixed;
  width: 800px;
  height: calc(100vh - 100px);
  right: 0;
  top: 80px;
  transition: right 0.3s ease-in-out;
}
</style>
