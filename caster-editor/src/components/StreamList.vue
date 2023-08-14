<script lang="ts" setup>
import { useStreamsSubscription } from "@/graphql";
import { ElButton, ElTable, ElTableColumn } from "element-plus";
import { useRouter } from "vue-router";

const router = useRouter();

const { data, fetching } = useStreamsSubscription({
  variables: {
    numOfStreams: 10,
  },
});
</script>

<template>
  <div
    v-loading="!fetching"
    class="streams-list"
  >
    <ElTable
      :data="data?.streams"
      style="width: 100%"
    >
      <ElTableColumn
        prop="uuid"
        label="UUID"
      />
      <ElTableColumn
        prop="modifiedDate"
        label="Last update"
      />
      <ElTableColumn
        prop="numListeners"
        label="Number of listeners"
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
                name: 'streamLogs',
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
