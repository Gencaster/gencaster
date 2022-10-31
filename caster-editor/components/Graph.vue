<!-- <script lang="ts">
import { defineComponent, toRefs, ref, reactive } from 'vue';
import { useGetGraphQuery, useCreateNodeMutation } from '../graphql/graphql';
import * as vNG from 'v-network-graph';
import { transformEdges, transformNodes } from '../tools/typeTransformers';

export default defineComponent({
  props: {
    uuid: String,
  },

  setup(props) {
    const uuid = toRefs(props).uuid;

    const selectedNodes = ref<string[]>([]);
    const selectedEdges = ref<string[]>([]);
    const configs = reactive(vNG.getFullConfigs());
    configs.node.selectable = true;

    const { executeMutation: newMutation } = useCreateNodeMutation();

    function addNode(event) {
      const singleid = Math.round(Math.random() * 1000000);
      console.log('start adding note', event);
      const variables = {
        graphUuid: uuid,
        name: `Some new random name ${singleid}`,
      };
      newMutation(variables).then(() => {
        console.log('Hello, we are finished');
      });
    }

    const result = useGetGraphQuery({
      variables: { uuid: uuid },
      requestPolicy: 'network-only',
    });

    const refresh = () => {
      console.log('Rerfresh');
      result.executeQuery();
    };

    return {
      fetching: result.fetching,
      data: result.data,
      error: result.error,
      transformEdges,
      transformNodes,
      selectedNodes,
      selectedEdges,
      configs,
      refresh,
      addNode,
      removeNode() {
        console.log('removeNode');
      },
    };
  },
});
</script> -->

<template>
  <div class="index-page">
    <div v-if="fetching">...Loading</div>
    <div v-else>
      <h1>
        Welcome to the Editor of <b>{{ data.graph.name }}</b>
      </h1>
      <div class="demo-control-panel">
        <div>
          <label>Node:</label>
          {{ data.graph.nodes.length }}
          <button :disabled="selectedNodes.length == 0" @click="removeNode()">
            remove
          </button>
          <button @click="addNode">Create</button>
        </div>
        <div>
          <label>Edge:</label>
          {{ data.graph.edges.length }}
        </div>
      </div>
      <br />
      <v-network-graph
        class="graph"
        :selected-nodes="selectedNodes"
        :nodes="transformNodes(data.graph.nodes)"
        :edges="transformEdges(data.graph.edges)"
        :configs="configs"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { useGetGraphQuery, useCreateNodeMutation } from '../graphql/graphql';
import * as vNG from 'v-network-graph';
import { transformEdges, transformNodes } from '../tools/typeTransformers';

export default {
  name: 'graphComponent',

  props: {
    uuid: {
      type: String,
      required: true,
    },
  },

  data() {
    return {
      fetching: true,
      result: null,
      data: null,
      error: null,

      // graph
      selectedNodes: <string[]>[],
      selectedEdges: <string[]>[],
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
        console.log('Added node');
      });
    },

    removeNode() {
      console.log('removeNode');
    },

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
    },
  },
};
</script>
