<script lang="ts" setup>
import { useGraphStore } from "@/stores/GraphStore";
import { storeToRefs } from "pinia";
import { computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import Graph from "@/components/Graph.vue";

const { graph, uuid, error } = storeToRefs(useGraphStore());

// router
const router = useRouter();

// get route
const route = useRoute();
const routeUUID = computed(() => String(route.params.uuid));

// set uuid
uuid.value = routeUUID.value;

watch(error, () => {
  if (error.value?.name === 'CombinedError') {
    router.push("/graphs");
  }
})
</script>

<template>
  <div
    v-if="graph"
    class="edit-page"
  >
    <Graph :uuid="route.params.uuid" />
  </div>
</template>
