<template>
  <div>
    <div v-if="fetching" class="fetching-screen">
      <elementsLoading />
    </div>
    <div v-else>
      <div v-if="data !== null">
        <h1>Select one of your Graphs</h1>
        <div class="demo-control-panel">
          <div>
            <br>
            <div v-for="graph in data?.graphs" :key="graph.uuid" class="graph-selection" :value="graph.uuid">
              <NuxtLink class="graph" :to="`../graphs/${graph.uuid}`">
                <div>
                  <p>{{ graph.name }}</p>
                </div>
                <div>
                  <p>{{ graph.uuid }}</p>
                </div>
              </NuxtLink>
            </div>
            <div class="graph-selection">
              <div class="graph new-one" @click="createNewGraph()">
                <div>
                  <p>+</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <p>You're not logged in.</p>
      </div>
      <br>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useGetGraphsQuery } from "@/graphql/graphql";
const { data, executeQuery, fetching, error } = await useGetGraphsQuery();

const createNewGraph = () => {
  alert("tbd");
};
</script>
