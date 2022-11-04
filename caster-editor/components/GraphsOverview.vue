<!-- <script lang="ts" setup>
import { Edit } from '@element-plus/icons-vue';
</script> -->
<!-- <el-switch v-model="value1" /> -->
<!-- <el-config-provider size="small">
      <el-button type="primary" :icon="Edit" />
    </el-config-provider> -->

<template>
  <div class="index-page">
    <div class="fetching-screen" v-if="fetching"><elementsLoading /></div>
    <div v-else>
      <h1>Please select a graph</h1>
      <div class="demo-control-panel">
        <div>
          <label><b>Graph</b></label>
          <form>
            <select v-model="selectedUuid">
              <option
                v-for="graph in graphsData.graphs"
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

<script lang="ts">
import { useGetGraphsQuery } from '../graphql/graphql';

export default {
  name: 'graphsOverviewComponent',

  data() {
    return {
      fetching: true,
      result: null,
      selectedUuid: null,
      graphsData: null,
    };
  },
  mounted() {
    this.initQuery();
  },
  methods: {
    async initQuery() {
      const result = await useGetGraphsQuery();

      this.result = result;
      this.graphsData = result.data;
      this.fetching = result.fetching;
      this.error = result.error;
    },
  },
};
</script>
