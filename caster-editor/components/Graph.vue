<!-- <script lang="ts">
import { defineComponent, toRefs, ref, reactive } from 'vue';
import { useGetGraphQuery, useCreateNodeMutation } from '../graphql/graphql';
import * as vNG from 'v-network-graph';
import { transformEdges, transformNodes } from '../tools/typeTransformers';
import * as Urql from '@urql/vue';

export default defineComponent({
  props: {
    uuid: String,
  },

  setup(props) {
    // access uuid
    const uuid = toRefs(props).uuid;

    // editor config
    const configs = reactive(vNG.getFullConfigs());
    configs.node.selectable = true;

    // setup node & edge data
    const selectedNodes = ref<string[]>([]);
    const selectedEdges = ref<string[]>([]);

    // const executeMutation = useCreateNodeMutation;
    const { executeMutation: updateGraph } = useCreateNodeMutation;
    console.log(useCreateNodeMutation);

    // const { executeMutation: updateTodo } = Urql.useMutation(`
    //   mutation ($id: ID!, $title: String!) {
    //     updateTodo (id: $id, title: $title) {
    //       id
    //       title
    //     }
    //   }
    // `);

    // load data
    const result = useGetGraphQuery({
      variables: { uuid: uuid },
      requestPolicy: 'network-only',
    });

    // data functions
    const refresh = () => {
      console.log('Rerfresh');
      result.executeQuery();
    };

    // interface  functions
    const addNode = async () => {
      try {
        const variables = { graphUuid: uuid, name: 'Some new random name' };
        // console.log(result);

        // // console.log(result.isPaused);
        // // result.pause();
        // console.log(result.isPaused);

        // console.log(executeMutation);

        // useCreateNodeMutation();

        // executeMutation()

        console.log(updateGraph);

        useCreateNodeMutation()
          .executeMutation(variables)
          .then(() => {
            // console.log('Please refresh');
            // refresh();
          });
      } catch (err) {
        console.log(err);
      }
    };

    const removeNode = async () => {
      console.log('removeNode');
    };

    // let isPaused = ref(false);

    // export for scope
    return {
      // isPaused,
      fetching: result.fetching,
      data: result.data,
      error: result.error,
      refresh() {
        result.executeQuery({
          requestPolicy: 'network-only',
        });
      },
      transformEdges,
      transformNodes,
      selectedNodes,
      selectedEdges,
      configs,
      updateGraph,
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
          <!-- <button @click="isPaused ? resume() : pause()">Toggle Query</button> -->
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

      <p>{{ data.graph }}</p>
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
      data: null,
      error: null,

      transformEdges,
      transformNodes,

      selectedNodes: [],
      selectedEdges: [],
      configs: vNG.getFullConfigs(),
    };
  },
  mounted() {
    console.log(this.uuid);

    this.configs.node.selectable = true;
    // const { executeMutation: newMutation } = useCreateNodeMutation;

    // get async data
    this.loadData();

    // setTimeout(() => {
    //   console.log(this.selectedNodes);
    // }, 2000);
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
      console.log(this.selectedNodes);
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
      const variables = { graphUuid: this.uuid, name: 'Some new random name' };

      try {
        useCreateNodeMutation()
          .executeMutation(variables)
          .then(() => {
            // console.log('Please refresh');
            // this.refresh();
          });
      } catch (err) {
        console.log(err);
      }
    },
  },
};
</script>
