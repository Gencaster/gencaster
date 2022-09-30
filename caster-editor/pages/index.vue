<script setup lang="ts">
import { reactive, ref } from 'vue';
import { Nodes, Edges } from 'v-network-graph';
import data from '~~/assets/data/graphData';

import { useQuery } from '@urql/vue';
import { MyQueryDocument } from '../graphql/graphql';

const nodes: Nodes = reactive({ ...data.nodes });
const edges: Edges = reactive({ ...data.edges });
const nextNodeIndex = ref(Object.keys(nodes).length + 1);
const nextEdgeIndex = ref(Object.keys(edges).length + 1);

const selectedNodes = ref<string[]>([]);
const selectedEdges = ref<string[]>([]);

const addNode = () => {
  const nodeId = `node${nextNodeIndex.value}`;
  const name = `N${nextNodeIndex.value}`;
  nodes[nodeId] = { name };
  nextNodeIndex.value++;
};

function removeNode() {
  for (const nodeId of selectedNodes.value) {
    delete nodes[nodeId];
  }
}

function addEdge() {
  if (selectedNodes.value.length !== 2) return;
  const [source, target] = selectedNodes.value;
  const edgeId = `edge${nextEdgeIndex.value}`;
  edges[edgeId] = { source, target };
  nextEdgeIndex.value++;
}

function removeEdge() {
  for (const edgeId of selectedEdges.value) {
    delete edges[edgeId];
  }
}

const loadData = () => {
  console.log('load needs to be written');
  MyQueryDocument;
};
</script>

<template>
  <div class="index-page">
    <div>
      <h1>Welcome to the Editor</h1>
      <br />
    </div>
    <div class="demo-control-panel">
      <div>
        <label>Node:</label>
        <button @click="addNode">add</button>
        <button :disabled="selectedNodes.length == 0" @click="removeNode">
          remove
        </button>
      </div>
      <div>
        <label>Edge:</label>
        <button :disabled="selectedNodes.length != 2" @click="addEdge">
          add
        </button>
        <button :disabled="selectedEdges.length == 0" @click="removeEdge">
          remove
        </button>
      </div>
    </div>
    <div class="second-panel">
      <button @click="loadData">Load Data</button>
    </div>
    <br />

    <v-network-graph
      class="graph"
      v-model:selected-nodes="selectedNodes"
      v-model:selected-edges="selectedEdges"
      :nodes="nodes"
      :edges="edges"
      :layouts="data.layouts"
      :configs="data.configs"
    />
  </div>
</template>
