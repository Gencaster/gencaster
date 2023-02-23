<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { ElTable } from "element-plus";

import { useGraphsStore } from "@/stores/Graphs";

const { graphs, selectedGraph, fetching } = storeToRefs(useGraphsStore());

const selectGraph = (index: number) => {
  selectedGraph.value = graphs.value?.graphs[index];
};
</script>

<template>
  <div>
    <ElTable
      v-loading="fetching"
      :data="graphs?.graphs"
      :default-sort="{ prop: 'name', order: 'ascending' }"
      style="width: 100%"
    >
      <el-table-column prop="name" label="Name" />
      <el-table-column prop="uuid" label="UUID" />
      <el-table-column fixed="right" label="Actions">
        <template #default="scope">
          <el-button
            link
            type="primary"
            size="small"
            @click.prevent="selectGraph(scope.$index)"
          >
            Select
          </el-button>
        </template>
      </el-table-column>
    </ElTable>
  </div>
</template>
