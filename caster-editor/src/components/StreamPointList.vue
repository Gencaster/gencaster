<script lang="ts" setup>
import { useStreamPointsQuery } from "@/graphql";
import { ElButton, ElTable, ElTableColumn } from "element-plus";
import { useRouter } from "vue-router";

const router = useRouter();

const { data, fetching } = useStreamPointsQuery();
</script>

<template>
  <div
    v-loading="fetching"
    class="streams-list"
  >
    <ElTable
      :data="data?.streamPoints"
      style="width: 100%"
    >
      <ElTableColumn
        prop="uuid"
        label="UUID"
      />
      <ElTableColumn
        prop="janusInPort"
        label="janusInPort"
      />
      <ElTableColumn
        fixed="right"
        label="Operations"
        width="120"
      >
        <template #default="scope">
          <ElButton
            type="primary"
            size="small"
            @click="
              router.push({
                name: 'streamPointLogs',
                params: { uuid: scope.row.uuid },
              })
            "
          >
            Logs
          </ElButton>
        </template>
      </ElTableColumn>
    </ElTable>
  </div>
</template>
