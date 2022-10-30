<!-- <script lang="ts">
import { defineComponent } from 'vue';
import { useQuery } from '@urql/vue';
import { useGetGraphsQuery } from '../graphql/graphql';

export default defineComponent({
  setup() {
    const result = useGetGraphsQuery();
    return {
      fetching: result.fetching,
      data: result.data,
      error: result.error,
    };
  },
  data() {
    return {
      selectedUuid: null,
    };
  },
});
</script> -->

<template>
  <div class="index-page">
    <div v-if="fetching">...Loading</div>
    <div v-else>
      <h1>Please select a graph</h1>
      <div class="demo-control-panel">
        <div>
          <label>Graph:</label>
          <form>
            <select v-model="selectedUuid">
              <option
                v-for="graph in data.graphs"
                :key="graph.uuid"
                :value="graph.uuid"
              >
                {{ graph.name }}
              </option>
            </select>
          </form>
        </div>
      </div>
      <br />
    </div>
    <div v-if="selectedUuid">
      <Graph :uuid="selectedUuid"></Graph>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { useQuery } from '@urql/vue';
import { useGetGraphsQuery } from '../graphql/graphql';

export default {
  name: 'graphsComponent',

  data() {
    return {
      fetching: true,
      selectedUuid: null,
    };
  },
  mounted() {
    this.initQuery();
  },
  methods: {
    async initQuery() {
      this.result = await useGetGraphsQuery();
      console.log(this.result);
    },
  },
};
</script>
