<template>
  <div>
    <div v-if="fetching" class="fetching-screen">
      <elementsLoading />
    </div>
    <div v-else>
      <div v-if="graphsData !== null">
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
import { useGetGraphsQuery } from "../graphql/graphql";

export default {
  name: "GraphsOverviewComponent",

  data() {
    return {
      fetching: true,
      result: null,
      graphsData: {
        graphs: [{
          uuid: "",
          name: ""
        }]
      }
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
        this.graphsData = result.data;
        this.fetching = result.fetching;
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
