<template>
  <div>
    <div class="fetching-screen" v-if="fetching">
      <elementsLoading />
    </div>
    <div v-else>
      <h1>Select one of your Graphs</h1>
      <div class="demo-control-panel">
        <div>
          <br />
          <div
            class="graph-selection"
            v-for="graph in graphsData.graphs"
            :key="graph.uuid"
            :value="graph.uuid"
          >
            <NuxtLink class="graph" :to="'graph/' + graph.uuid">
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
      <br />
    </div>
  </div>
</template>

<script lang="ts">
import { useGetGraphsQuery } from '../graphql/graphql';

export default {
  name: 'graphsOverviewComponent',

  data() {
    return {
      fetching: true,
      result: null,
      graphsData: null,
    };
  },
  mounted() {
    this.initQuery();
  },
  methods: {
    async initQuery() {
      const result = await useGetGraphsQuery();

      this.result = result;
      this.graphsData = result.data;
      this.fetching = result.fetching;
      this.error = result.error;
    },

    createNewGraph() {
      alert('tbd');
    },
  },
};
</script>
