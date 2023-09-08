<script setup lang="ts">
import Bars from "@/components/PlayerVisualizer/PlayerVisualizerBars.vue";
</script>

<template>
  <div class="visualizer-wrapper general-padding">
    <Bars />
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/mixins.scss";
@import "@/assets/variables.scss";

.visualizer-wrapper {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
}
</style>
