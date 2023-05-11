<script lang="ts" setup>
import { ElTable, ElTableColumn } from "element-plus";
import { useRouter } from "vue-router";
import { useGetGraphsQuery } from "@/graphql";

const router = useRouter();
const { data, fetching } = useGetGraphsQuery();
</script>

<template>
  <div class="graphs-wrapper">
    <div class="graphs">
      <h1>Alle Graphen</h1>
      <Transition>
        <ElTable v-if="data" v-loading="fetching" :data="data?.graphs" :default-sort="{ prop: 'name', order: 'ascending' }">
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
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/variables.scss';

  .graphs {
    margin: 0 auto;
    padding-top: $spacingS;
    width: calc(100% - 2 * $mobilePadding);
    max-width: $desktopMaxWidth;
  }
</style>
