<script setup lang="ts">
import Bars from "@/components/PlayerVisualizer/PlayerVisualizerBars.vue";
</script>

<template>
  <div class="visualizer-wrapper">
    <Bars />
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

.visualizer-wrapper {
  width: 100%;
  height: 100%;
}
</style>
