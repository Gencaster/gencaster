<template>
  <div>
    <div v-if="fetching" class="fetching-screen">
      <elementsLoading />
    </div>
    <div v-else>
      <div v-if="result !== null">
        <h1>Select one of your Graphs</h1>
        <div class="demo-control-panel">
          <div>
            <br>
            <div v-for="graph in graphsData.graphs" :key="graph.uuid" class="graph-selection" :value="graph.uuid">
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

<script lang="ts">
// import type { GetGraphsQuery } from "@/graphql/graphql";
import type { GetGraphsQuery } from "@/graphql/graphql";
import { useGetGraphsQuery } from "@/graphql/graphql";

export default {
  name: "GraphsOverviewComponent",

  data() {
    return {
      fetching: true as boolean,
      result: {},
      graphsData: {},
      error: {}
      // TODO: import the correct types. Somehow GetGraphsQuery is not working
    };
  },
  mounted() {
    this.initQuery();
  },
  methods: {
    async initQuery() {
      try {
        const result = await useGetGraphsQuery();
        this.result = result;
        this.fetching = result.fetching.value;
        this.graphsData = result.data;
        this.error = result.error;
      }
      catch (error) {
        console.log("not allowed");
      }
    },

    createNewGraph() {
      alert("tbd");
    }
  }
};
</script>
