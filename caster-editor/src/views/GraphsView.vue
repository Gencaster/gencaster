<script setup lang="ts">
import GraphsList from "@/components/GraphsList.vue";
import { useGetGraphsQuery } from "@/graphql";
import Loading from "@/components/Loading.vue";

const { data, error, fetching } = useGetGraphsQuery();
</script>

<template>
  <div v-if="error">
    <h3>Please login</h3>
  </div>
  <div
    v-else-if="fetching"
    class="fetching-screen"
  >
    <Loading />
  </div>
  <div v-else-if="!data">
    <h3>No graphs to display</h3>
  </div>
  <div v-else>
    <GraphsList
      :graphs="data.graphs"
      class="graphs-overview-page"
    />
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/scss/variables.module.scss";

.graphs-overview-page {
  padding: 10px 15px 10px 15px;
}
</style>
