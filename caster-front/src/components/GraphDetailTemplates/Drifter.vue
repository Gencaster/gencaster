<script setup lang="ts">
import GraphPlayer from "@/components/GraphPlayer.vue";
import type { Graph } from "@/graphql";

defineProps<{
  graph: Pick<Graph, "uuid" | "name">
}>();
</script>

<template>
  <div class="default-graph-detail">
    <h1>Drifter</h1>
    <GraphPlayer
      :graph="graph"
    />
  </div>
</template>
