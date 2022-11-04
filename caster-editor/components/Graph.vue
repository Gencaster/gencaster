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
          <button @click="addNode">Add Node</button>
          <button @click="addEdge">Add Edge</button>
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
import {
  useGetGraphQuery,
  useCreateNodeMutation,
  useCreateEdgeMutation,
} from '../graphql/graphql';
import * as vNG from 'v-network-graph';
import { Nodes, Edges } from 'v-network-graph';
import { GraphSettings } from '~/assets/js/graphSettings';

import { transformEdges, transformNodes } from '../tools/typeTransformers';

export default {
  name: 'graphComponent',

  props: {
    uuid: {
      type: String,
      required: true,
    },
  },

  computed: {},

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
      nextNodeIndex: 0,
      nextEdgeIndex: 0,
      transformEdges,
      transformNodes,
      configs: vNG.getFullConfigs(),
    };
  },

  mounted() {
    this.configs.node.selectable = true;
    const { executeMutation: addNodeMutation } = useCreateNodeMutation();
    this.addNodeMutation = addNodeMutation;

    const { executeMutation: addEdgeMutation } = useCreateEdgeMutation();
    this.addEdgeMutation = addEdgeMutation;

    this.configs = GraphSettings.standard;

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

      this.nextNodeIndex = Object.keys(this.nodes).length + 1;
      this.nextEdgeIndex = Object.keys(this.edges).length + 1;
    },

    refresh() {
      this.result.executeQuery();
    },

    addNode() {
      const singleid = Math.round(Math.random() * 1000000);
      console.log('start adding note');
      const variables = {
        graphUuid: this.uuid,
        name: `${singleid}`,
      };
      this.addNodeMutation(variables).then(() => {
        this.refresh();
        console.log('Added node');
      });
    },

    addEdge() {
      if (this.selectedNodes.length !== 2) {
        alert('requires exactly 2 nodes selected');
        return;
      }
      const [source, target] = this.selectedNodes;

      console.log(source, target);

      const variables = {
        nodeInUuid: source,
        nodeOutUuid: target,
      };

      this.addEdgeMutation(variables).then(() => {
        this.refresh();
        console.log('Added edge');
      });

      // const edgeId = `edge${this.nextEdgeIndex}`;
      // this.nextEdgeIndex++;
    },

    removeNode() {
      if (this.selectedNodes > 1) {
        alert('please only delete one at a time');
      } else {
        const variables = {
          uuid: this.selectedNodes[0],
        };

        // this.removeNodeMutation(variables).then(() => {
        //   this.refresh();
        //   console.log('Removed node');
        // });
      }
    },
  },
};
</script>
