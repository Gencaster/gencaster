<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useStreamPointsStore } from "@/stores/StreamPoints";

const { streamPoints, fetching, selectedStreamPoint } = storeToRefs(useStreamPointsStore());

const selectStreamPoint = (index: number) => {
  selectedStreamPoint.value = streamPoints.value?.streamPoints[index];
};
</script>

<template>
  <ElTable
    v-loading="fetching"
    :data="streamPoints?.streamPoints"
    style="width: 100%"
    :default-sort="{ prop: 'port', order: 'ascending' }"
  >
    <el-table-column prop="port" label="Port" />
    <el-table-column prop="janusInRoom" label="In room" />
    <el-table-column prop="janusOutRoom" label="Out room" />
    <el-table-column prop="uuid" label="UUID" />
    <el-table-column fixed="right" label="Actions">
      <template #default="scope">
        <el-button
          link
          type="primary"
          size="small"
          @click.prevent="selectStreamPoint(scope.$index)"
        >
          Select
        </el-button>
      </template>
    </el-table-column>
  </ElTable>
</template>
