<template>
  <div class="edit-page">
    <div class="editor-wrapper">
      <div class="editor-inner">
        <div class="node-data">
          <ElementsNodeEditor :dev="true" node-uuid="debugnode" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { debugScriptCells, emptyNode } from "@/assets/js/dev/debugBlockData";
import { useGraphStore } from "@/stores/GraphStore";

// Store
const graphStore = useGraphStore();

// commit the node data to the store
graphStore.graphUserState.nodes.debugnode = emptyNode;
graphStore.graphUserState.nodes.debugnode.scriptCells = debugScriptCells;
</script>

<style lang="scss">
.edit-page {
  .editor-wrapper {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    background-color: white;
    width: 100vw;
    height: 100vh;
    padding: 20px;

    .editor-inner {
      width: 50%;
      width: 800px;
      height: 100%;
    }
  }
}
</style>
