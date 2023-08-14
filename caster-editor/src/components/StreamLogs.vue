<script lang="ts" setup>
import type { StreamLogsSubscription } from "@/graphql";
import { useStreamLogsSubscription, type StreamLog } from "@/graphql";
import { ElTable, ElTableColumn } from "element-plus";
import { ref, toRef, type Ref } from "vue";

const props = defineProps<{
  streamPointUuid?: string;
  streamUuid?: string;
}>();

const logs: Ref<
  Pick<StreamLog, "uuid" | "createdDate" | "level" | "message">[]
> = ref([]);

const { fetching } = useStreamLogsSubscription(
  {
    variables: {
      streamUuid: toRef(props, "streamUuid"),
      streamPointUuid: toRef(props, "streamPointUuid"),
    },
  },
  (_: any, newInfo: StreamLogsSubscription) => {
    logs.value.push(newInfo.streamLogs);
  },
);
</script>

<template>
  <div
    v-loading="!fetching"
    class="stream-logs"
  >
    <ElTable
      :data="logs"
      style="width: 100%"
    >
      <ElTableColumn
        prop="createdDate"
        label="Time"
        width="300"
      />
      <ElTableColumn
        prop="level"
        label="Level"
        width="75"
      />
      <ElTableColumn
        prop="message"
        label="Message"
      />
    </ElTable>
  </div>
</template>
