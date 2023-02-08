<script lang="ts" setup>
import { useGraphStore } from "@/stores/GraphStore";
import { storeToRefs } from "pinia";
import { computed } from "vue";
import { useRoute } from "vue-router";
import Graph from "@/components/Graph.vue";

const { graph, uuid } = storeToRefs(useGraphStore());

// get route
const route = useRoute();
const routeUUID = computed(() => String(route.params.uuid));

// set uuid
uuid.value = routeUUID.value;
</script>

<template>
  <div
    v-if="graph"
    class="edit-page"
  >
    <Graph :uuid="route.params.uuid" />
  </div>
</template>
