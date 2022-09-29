<template class="index-page">
  <div>
    <h1>Welcome to the Editor</h1>
  </div>
  <v-network-graph class="graph" :nodes="nodes" :edges="edges" />
</template>

<script setup lang="ts">
const nodes = {
  node1: { name: 'Node 1' },
  node2: { name: 'Node 2' },
  node3: { name: 'Node 3' },
  node4: { name: 'Node 4' },
};

const edges = {
  edge1: { source: 'node1', target: 'node2' },
  edge2: { source: 'node2', target: 'node3' },
  edge3: { source: 'node3', target: 'node4' },
};
</script>

<style>
.graph {
  width: 800px;
  height: 600px;
  border: 1px solid #000;
}
</style>
