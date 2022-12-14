<template>
  <div class="edit-page">
    <div class="editor-wrapper">
      <div class="editor-inner">
        <div class="node-data">
          <ElementsBlockEditor :dev="true" :blocks-data="debugBlockData" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { debugBlockData } from "@/assets/js/dev/debugBlockData";
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
