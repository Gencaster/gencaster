<!-- <script lang="ts" setup>
import { Edit } from '@element-plus/icons-vue';
</script> -->
<!-- <el-switch v-model="value1" /> -->
<!-- <el-config-provider size="small">
      <el-button type="primary" :icon="Edit" />
    </el-config-provider> -->

<template>
  <div class="index-page">
    <div v-if="fetching"><elementsLoading /></div>
    <div v-else>
      <h1>
        Editing: <b>{{ data.graph.name }}</b>
        <br />
        <br />
      </h1>
      <div class="demo-control-panel">
        <div class="constol-btns">
          <p><b>Controls</b></p>
          <button :disabled="selectedNodes.length == 0" @click="removeNode()">
            Remove
          </button>
          <button @click="addNode">Add</button>
        </div>
      </div>
      <br />
      <v-network-graph
        class="graph"
        v-model:selected-nodes="selectedNodes"
        v-model:selected-edges="selectedEdges"
        :nodes="nodes"
        :edges="transformEdges(data.graph.edges)"
        :configs="configs"
      />

      <div class="stats">
        <p><b>Stats</b></p>
        <p>Nodes: {{ data.graph.nodes.length }}</p>
        <p>Edges: {{ data.graph.edges.length }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { useGetGraphQuery, useCreateNodeMutation } from '../graphql/graphql';
import * as vNG from 'v-network-graph';
import { Nodes, Edges } from 'v-network-graph';
import { transformEdges, transformNodes } from '../tools/typeTransformers';

export default {
  name: 'graphComponent',

  props: {
    uuid: {
      type: String,
      required: true,
    },
  },

  computed: {
    // nodes() {
    //   return transformNodes(this.data.graph.nodes);
    // },
  },

  data() {
    return {
      fetching: true,
      result: null,
      data: null,
      error: null,

      // graph
      nodes: {},
      edges: {},
      selectedNodes: [],
      selectedEdges: [],
      transformEdges,
      transformNodes,
      configs: vNG.getFullConfigs(),
    };
  },
  mounted() {
    this.configs.node.selectable = true;
    const { executeMutation: newMutation } = useCreateNodeMutation();
    this.newMutation = newMutation;

    this.loadData();
  },
  methods: {
    async loadData() {
      const result = await useGetGraphQuery({
        variables: { uuid: this.uuid },
        requestPolicy: 'network-only',
      });

      this.result = result;
      this.data = result.data;
      this.error = result.error;
      this.fetching = result.fetching;

      console.log('loaded graph');
      this.loadedData();
    },

    loadedData() {
      // set data
      this.nodes = transformNodes(this.data.graph.nodes);
      this.edges = transformNodes(this.data.graph.edges);
    },

    refresh() {
      this.result.executeQuery();
    },

    addNode(event) {
      const singleid = Math.round(Math.random() * 1000000);
      console.log('start adding note', event);
      const variables = {
        graphUuid: this.uuid,
        name: `Some new random name ${singleid}`,
      };
      this.newMutation(variables).then(() => {
        this.refresh();
        console.log('Added node');
      });
    },

    removeNode() {
      if (this.selectedNodes > 1) {
        alert('please only delete one at a time');
      } else {
        const variables = {
          uuid: this.selectedNodes[0],
        };

        this.newMutation(variables).then(() => {
          this.refresh();
          console.log('Removed node');
        });
      }
    },
  },
};
</script>
