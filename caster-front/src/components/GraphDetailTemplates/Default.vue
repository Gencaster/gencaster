<script setup lang="ts">
import GraphPlayer from "@/components/GraphPlayer.vue";
import type { Graph } from "@/graphql";

defineProps<{
  graph: Pick<Graph, "uuid" | "name">
}>();
</script>

<template>
  <div class="default-graph-detail">
    <GraphPlayer
      :graph="graph"
    />
  </div>
</template>

<style lang="scss" scoped>
.default-graph-detail {
  background-color: yellow;
}
</style>
