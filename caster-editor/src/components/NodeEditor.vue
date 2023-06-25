<template>
  <div class="node-editor">
    <NodeEditorHeader
      :node="node"
      @save-node="emit('saveNode')"
    />
    <div class="editor-header-spacer" />
    <NodeEditorCells v-model:script-cells="scriptCells" />
    <NodeEditorDevInfo
      :node="node"
    />
  </div>
</template>

<script setup lang="ts">
import NodeEditorHeader from "@/components/NodeEditorHeader.vue";
import NodeEditorDevInfo from "@/components/NodeEditorDevInfo.vue";

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
    let nodeUpdate = { ...props.node };
    nodeUpdate.scriptCells = value;
    emit('update:node', nodeUpdate);
    return value;
  },
});

</script>

<style lang="scss" scoped>
@import '@/assets/scss/variables.module.scss';

.node-editor {
  z-index: 1;
  background-color: white;
  position: fixed;
  width: 800px;
  height: calc(100vh - 100px);
  right: calc($menuHeight * 0.5);
  top: calc(2.5 * $menuHeight);
  transition: right 0.3s ease-in-out;
  overflow-x: hidden;
  border: 1px solid $black;
}

.editor-header-spacer {
  width: inherit;
  height: calc($menuHeight*2);
  margin-bottom: 30px;
}
</style>
