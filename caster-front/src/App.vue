<script setup lang="ts">
import { RouterView } from "vue-router";
</script>

<template>
  <div class="gencaster-frontend">
    <RouterView />
  </div>
</template>

<style lang="scss" scoped>
.gencaster-frontend {
  width: 100%;
  height: 100%;
  max-height: 100%;
  overflow-y: scroll;
}
</style>
