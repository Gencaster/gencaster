<script setup lang="ts">
import type { StreamPoint } from "@/graphql";
import { useStreamPointsQuery } from "@/graphql";

const emit = defineEmits<{
  (e: "selectedStreamPoint", streamPointUUID: StreamPoint): void
}>();

const { data, fetching } = useStreamPointsQuery();
</script>

<template>
  <ElTable
    v-loading="fetching"
    :data="data?.streamPoints"
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
          @click.prevent="emit('selectedStreamPoint', scope.row.uuid)"
        >
          Select
        </el-button>
      </template>
    </el-table-column>
  </ElTable>
</template>
