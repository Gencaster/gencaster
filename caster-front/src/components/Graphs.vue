<script lang="ts" setup>
import { ElContainer, ElMain, ElTable, ElTableColumn } from "element-plus";
import { useRouter } from "vue-router";
import { useGetGraphsQuery } from "@/graphql";

const router = useRouter();
const { data, fetching } = useGetGraphsQuery();
</script>

<template>
  <div class="common-layout">
    <ElContainer justify="center">
      <ElMain>
        <h1>Alle Graphen</h1>
        <Transition>
          <ElTable
            v-if="data" v-loading="fetching" :data="data?.graphs"
            :default-sort="{ prop: 'name', order: 'ascending' }"
          >
            <ElTableColumn label="Titel" sortable prop="name">
              <template #default="scope">
                <el-button
                  link size="small"
                  @click.prevent="$router.push({ name: 'graphPlayer', params: { graphName: scope.row.name } })"
                >
                  {{ scope.row.name }}
                </el-button>
              </template>
            </ElTableColumn>
          </ElTable>
        </Transition>
      </ElMain>
    </ElContainer>
  </div>
</template>
