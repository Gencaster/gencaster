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

    const { executeMutation: newMutation } = useCreateNodeMutation;

    const result = useGetGraphQuery({
      variables: { uuid: uuid },
      requestPolicy: 'network-only',
    });

    const refresh = () => {
      console.log('Rerfresh');
      result.executeQuery();
    };

    const removeNode = async () => {
      console.log('removeNode');
    };

    const addNode = async () => {
      console.log('addNode');
      const variables = { graphUuid: uuid, name: 'Some new random name' };
      useCreateNodeMutation()
        .executeMutation(variables)
        .then(() => {
          console.log('Please refresh');
          refresh();
        });
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
      removeNode,
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
          <button :disabled="selectedNodes.length == 0" @click="removeNode">
            Remove
          </button>
          <button @click="addNode">Add</button>
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
import { defineComponent, toRefs, ref, reactive } from 'vue';
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
      data: null,
      error: null,

      transformEdges,
      transformNodes,

      selectedNodes: ref<string[]>([]),
      selectedEdges: ref<string[]>([]),
      configs: vNG.getFullConfigs(),
    };
  },
  mounted() {
    console.log(this.uuid);

    this.configs.node.selectable = true;
    // const { executeMutation: newMutation } = useCreateNodeMutation;

    // get async data
    this.loadData();
  },
  methods: {
    async loadData() {
      const result = await useGetGraphQuery({
        variables: { uuid: this.uuid },
        requestPolicy: 'network-only',
      });

      this.data = result.data;
      this.error = result.error;
      this.fetching = result.fetching;

      console.log(result);
    },

    refresh() {
      console.log('Rerfresh');
      this.result.executeQuery();
    },

    async removeNode() {
      console.log('removeNode');
    },

    async addNode() {
      console.log('addNode');
    },
  },
};
</script>
