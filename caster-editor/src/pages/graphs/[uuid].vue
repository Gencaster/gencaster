<template>
  <div v-if="graphStore.graph" class="edit-page">
    <Graph :uuid="uuid" />
  </div>
</template>

<script lang="ts" setup>
import { useGraphStore } from "@/stores/GraphStore";

const graphStore = useGraphStore();

const route = useRoute();
const uuid = computed(() => String(route.params.uuid));

function getGraphData() {
  console.log("Should change graph uuid now!");
  graphStore.uuid = uuid.value;
}

watch(uuid, getGraphData);

getGraphData();
</script>
