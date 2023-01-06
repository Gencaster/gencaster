<template>
  <div v-if="!graphStore.fetching" class="edit-page">
    <Graph :uuid="uuid" />
  </div>
</template>

<script lang="ts" setup>
import { useGraphStore } from "@/stores/GraphStore";

const graphStore = useGraphStore();

const route = useRoute();
const uuid = computed(() => String(route.params.uuid));

function getGraphData() {
  graphStore.getGraph(uuid.value);
}

// how do we update the data?
watch(uuid, getGraphData);

getGraphData();
</script>
