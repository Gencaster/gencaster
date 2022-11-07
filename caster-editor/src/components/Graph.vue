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
        <div class="control">
          <p><b>Controls</b></p>
          <div class="row">
            <el-button text bg @click="addNode()">Add Node</el-button>
            <el-input v-model="newNodeName" placeholder="New Node Name" />
            <el-button text bg @click="addEdge()">Add Edge</el-button>
          </div>

          <div class="row">
            <el-button
              text
              bg
              :disabled="selectedNodes.length == 0"
              @click="removeNode()"
              >Remove Node</el-button
            >
            <el-button
              text
              bg
              :disabled="selectedEdges.length == 0"
              @click="removeEdge()"
              >Remove Edge</el-button
            >
          </div>
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
  useDeleteNodeMutation,
  useDeleteEdgeMutation,
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
      selectedNodes: new Array<string>(),
      selectedEdges: new Array<string>(),
      nextNodeIndex: 0,
      nextEdgeIndex: 0,
      transformEdges,
      transformNodes,
      configs: vNG.getFullConfigs(),

      // interface
      newNodeName: '',
    };
  },

  mounted() {
    this.configs.node.selectable = true;

    // add node
    const { executeMutation: addNodeMutation } = useCreateNodeMutation();
    this.addNodeMutation = addNodeMutation;

    // remove node
    const { executeMutation: removeNodeMutation } = useDeleteNodeMutation();
    this.removeNodeMutation = removeNodeMutation;

    // add edge
    const { executeMutation: addEdgeMutation } = useCreateEdgeMutation();
    this.addEdgeMutation = addEdgeMutation;

    // remove edge
    const { executeMutation: removeEdgeMutation } = useDeleteEdgeMutation();
    this.removeEdgeMutation = removeEdgeMutation;

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
      this.edges = transformEdges(this.data.graph.edges);

      this.nextNodeIndex = Object.keys(this.nodes).length + 1;
      this.nextEdgeIndex = Object.keys(this.edges).length + 1;
    },

    refresh() {
      this.result.executeQuery();
    },

    addNode() {
      if (this.newNodeName === '') {
        alert('please add a name for your node');
        return;
      }

      const variables = {
        graphUuid: this.uuid,
        name: this.newNodeName,
      };
      this.addNodeMutation(variables).then(() => {
        this.refresh();
        console.log('Added node');
      });

      this.newNodeName = '';
    },

    addEdge() {
      if (this.selectedNodes.length !== 2) {
        alert('requires exactly 2 nodes selected');
        return;
      }
      const [source, target] = this.selectedNodes;

      const variables = {
        nodeInUuid: source,
        nodeOutUuid: target,
      };

      this.addEdgeMutation(variables).then(() => {
        this.refresh();
        console.log('Added edge');
      });
    },

    removeNode() {
      for (const nodeId of this.selectedNodes) {
        const variables = {
          nodeUuid: nodeId,
        };

        this.removeNodeMutation(variables).then(() => {
          this.refresh();
          console.log('Removed node');
        });
      }
    },

    removeEdge() {
      for (const edgeId of this.selectedEdges) {
        const variables = {
          edgeUuid: edgeId,
        };

        this.removeEdgeMutation(variables).then(() => {
          this.refresh();
          console.log('Removed edge');
        });
      }
    },
  },
};
</script>
