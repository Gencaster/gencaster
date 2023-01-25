<template>
  <div v-if="graph" class="edit-page">
    <Graph :uuid="routeUUID" />
  </div>
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { useNuxtApp } from "#app";
const nuxtApp = useNuxtApp();

// store
const graphStore = nuxtApp.graphStore;
const { graph, uuid } = storeToRefs(graphStore);

// get route
const route = useRoute();
const routeUUID = computed(() => String(route.params.uuid));

// set uuid
uuid.value = routeUUID.value;
</script>
