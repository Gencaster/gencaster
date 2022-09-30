<script lang="ts">
import { Nodes, Edges } from 'v-network-graph';
import { defineComponent } from 'vue';
import { useQuery } from '@urql/vue';
import { useTestQueryQuery } from '../graphql/graphql';


export default defineComponent({
  setup() {
    const result = useTestQueryQuery();
    return {
      fetching: result.fetching,
      data: result.data,
      error: result.error,
    }
  }
});
</script>

<template>
  <div class="index-page">
    <div v-if="fetching">
      ...Loading
    </div>
    <div v-else>
      <h1>Welcome to the Editor of {{ data.graphs[0].name }}</h1>
    <div class="demo-control-panel">
      <div>
        <label>Node:</label>
        {{ data.graphs[0].nodes }}
      </div>
      <div>
        <label>Edge:</label>
        {{ data.graphs[0].edges }}
      </div>
    </div>
    <br />
    <v-network-graph
      class="graph"
      :nodes=data.graphs[0].nodes
      :edges=data.graphs[0].edges
    />
    </div>
  </div>
</template>
