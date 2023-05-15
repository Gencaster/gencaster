<script setup lang="ts">
import { ElButton, ElTable, ElTableColumn } from "element-plus";
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
    <ElTableColumn prop="port" label="Port" />
    <ElTableColumn prop="janusInRoom" label="In room" />
    <ElTableColumn prop="janusOutRoom" label="Out room" />
    <ElTableColumn prop="uuid" label="UUID" />
    <ElTableColumn fixed="right" label="Actions">
      <template #default="scope">
        <ElButton
          link
          type="primary"
          size="small"
          @click.prevent="emit('selectedStreamPoint', scope.row)"
        >
          Select
        </ElButton>
      </template>
    </ElTableColumn>
  </ElTable>
</template>
