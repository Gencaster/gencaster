<script lang="ts" setup>
import { ElTable, ElTableColumn } from "element-plus";
import { useRouter } from "vue-router";
import { useGetGraphsQuery } from "@/graphql";

const router = useRouter();
const { data, fetching } = useGetGraphsQuery();
</script>

<template>
  <div>
    <ElTable
      v-loading="fetching"
      :data="data?.graphs"
      :default-sort="{ prop: 'name', order: 'ascending' }"
    >
      <ElTableColumn label="Graph name" sortable prop="name">
        <template #default="scope">
          <el-button
            link
            size="small"
            @click.prevent="$router.push({ name: 'graphPlayer', params: { graphName: scope.row.name } })"
          >
            {{ scope.row.name }}
          </el-button>
        </template>
      </ElTableColumn>
    </ElTable>
  </div>
</template>
