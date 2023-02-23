<script setup lang="ts">
import { storeToRefs } from "pinia";
import { watch } from "vue";
import Graphs from "@/components/Graphs.vue";
import { useGraphsStore } from "@/stores/Graphs";
import router from "@/router/index";

const { selectedGraph } = storeToRefs(useGraphsStore());

watch(selectedGraph, () => {
  if (selectedGraph.value === undefined)
    return;
  router.push({ name: "graphPlayer", params: { graphUuid: selectedGraph.value.uuid } });
});
</script>

<template>
  <main>
    <h1>Welcome to Gencaster</h1>
    <!-- @todot min-width is a hack b/c otherwise the div will not grow after loading -->
    <Graphs :style="{ 'min-width': '800px' }" />
  </main>
</template>
