<template>
  <div>
    <div v-if="graphsStore.fetching" class="fetching-screen">
      <elementsLoading />
    </div>
    <div v-else>
      <div v-if="graphsStore.graphs.length > 0">
        <h1>Select one of your Graphs</h1>
        <div class="demo-control-panel">
          <div>
            <br>
            <div v-for="graph in graphsStore.graphs" :key="graph.uuid" class="graph-selection" :value="graph.uuid">
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
import { useGraphsStore } from "@/stores/GraphsStore";
const graphsStore = useGraphsStore();

const createNewGraph = () => {
  alert("tbd");
};
</script>
