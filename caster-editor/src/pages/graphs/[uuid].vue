<script lang="ts" setup>
import { useGetGraphQuery } from "~~/src/graphql/graphql";

const route = useRoute();
const uuid = computed(() => String(route.params.uuid));

const { data, executeQuery, fetching, error } = await useGetGraphQuery({
  variables: { uuid },
  requestPolicy: "network-only"
});

if (error.value)
  throw createError({ statusCode: 404, statusMessage: "Hello", fatal: true });

const graph = computed(() => data.value?.graph);
</script>

<template>
  <div v-if="fetching">
    <elementsLoading />
  </div>
  <div v-else class="edit-page">
    <Graph v-if="graph" :graph="graph" />
    <!-- <Graph :uuid="uuid" /> -->
  </div>
</template>
