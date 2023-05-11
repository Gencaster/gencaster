<script setup lang="ts">
import GraphPlayer from "@/components/GraphPlayer.vue";
import type { Graph } from "@/graphql";

defineProps<{
  graph: Pick<Graph, "uuid" | "name">
}>();
</script>

<template>
  <div class="default-graph-detail">
    <p>Dast ist ein test</p>
    <GraphPlayer
      :graph="graph"
    />
  </div>
</template>
