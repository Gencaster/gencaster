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
