<template>
  <div class="index-page">
    <div v-if="fetching">...Loading</div>
    <div v-else>
      <h1>
        Welcome to the Editor of <b>{{ data.graph.name }}</b>
        <br />
        <br />
      </h1>
      <div class="demo-control-panel">
        <div class="constol-btns">
          <p><b>Controls</b></p>
          <button :disabled="selectedNodes.length == 0" @click="removeNode()">
            Remove
          </button>
          <button @click="addNode">Create</button>
        </div>
        <div class="stats">
          <p><b>Stats</b></p>
          <p>Nodes: {{ data.graph.nodes.length }}</p>
          <p>Edges: {{ data.graph.edges.length }}</p>
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
import { useGetGraphQuery, useCreateNodeMutation } from '../graphql/graphql'
import * as vNG from 'v-network-graph'
import { transformEdges, transformNodes } from '../tools/typeTransformers'

export default {
  name: 'graphComponent',

  props: {
    uuid: {
      type: String,
      required: true
    }
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
      configs: vNG.getFullConfigs()
    }
  },
  mounted() {
    this.configs.node.selectable = true
    const { executeMutation: newMutation } = useCreateNodeMutation()
    this.newMutation = newMutation

    this.loadData()
  },
  methods: {
    refresh() {
      this.result.executeQuery()
    },

    addNode(event) {
      const singleid = Math.round(Math.random() * 1000000)
      console.log('start adding note', event)
      const variables = {
        graphUuid: this.uuid,
        name: `Some new random name ${singleid}`
      }
      this.newMutation(variables).then(() => {
        console.log('Added node')
        this.refresh()
      })
    },

    removeNode() {
      console.log('removeNode')
    },

    async loadData() {
      const result = await useGetGraphQuery({
        variables: { uuid: this.uuid },
        requestPolicy: 'network-only'
      })

      this.result = result
      this.data = result.data
      this.error = result.error
      this.fetching = result.fetching

      console.log('loaded graph')
    }
  }
}
</script>
