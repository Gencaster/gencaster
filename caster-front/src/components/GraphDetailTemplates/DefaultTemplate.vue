<script setup lang="ts">
import GraphPlayer from "@/components/GraphPlayer.vue";
import type { Graph } from "@/graphql";

defineProps<{
  graph: Pick<
    Graph,
    | "uuid"
    | "name"
    | "aboutText"
    | "displayName"
    | "startText"
    | "endText"
    | "slugName"
  >;
}>();
</script>

<template>
  <div class="default-graph-detail">
    <GraphPlayer
      :graph="graph"
      :show-debug="true"
    />
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/mixins.scss";
@import "@/assets/variables.scss";

.default-graph-detail {
  position: relative;
  box-sizing: border-box;
  width: 100%;
  height: 100vh;
}
</style>
