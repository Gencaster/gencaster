<template>
  <div v-if="fetching">
    <elementsLoading />
  </div>
  <div v-else class="edit-page">
    <Graph v-if="graph" :uuid="uuid" :graph="graph" />
  </div>
</template>

<script lang="ts" setup>
import { useGetGraphQuery } from "@/graphql/graphql";
import { useGraphStore } from "@/stores/GraphStore";

// Store
const graphStore = useGraphStore();

const route = useRoute();
const uuid = computed(() => String(route.params.uuid));

const { data, executeQuery, fetching, error } = await useGetGraphQuery({
  variables: { uuid },
  requestPolicy: "network-only"
});

graphStore.updateData(data.value);
graphStore.updateQuery(executeQuery);

if (error.value)
  throw createError({ statusCode: 404, statusMessage: "Error Loading", fatal: true });

const graph = computed(() => data.value?.graph);
</script>
