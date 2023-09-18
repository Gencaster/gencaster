<script lang="ts" setup>
import type { StreamLogsSubscription } from "@/graphql";
import { useStreamLogsSubscription, type StreamLog, LogLevel } from "@/graphql";
import { Scope } from "@sentry/vue";
import { ElTable, ElTableColumn, ElTag } from "element-plus";
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

const convertLogLevelType = (
  level: string,
): "success" | "info" | "warning" | "danger" | "" => {
  switch (level) {
    case LogLevel.Critical: {
      return "danger";
    }
    case LogLevel.Error: {
      return "danger";
    }
    case LogLevel.Warning: {
      return "warning";
    }
    case LogLevel.Info: {
      return "success";
    }
    case LogLevel.Debug: {
      return "info";
    }
    default: {
      return "";
    }
  }
};

const formatDate = (date: string): string => {
  return new Date(date).toLocaleString("sv-SE");
};
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
        width="170"
      >
        <template #default="scope">
          {{ formatDate(scope.row.createdDate) }}
        </template>
      </ElTableColumn>
      <ElTableColumn
        prop="level"
        label="Level"
        width="75"
      >
        <template #default="scope">
          <ElTag :type="convertLogLevelType(scope.row.level)">
            {{ scope.row.level }}
          </ElTag>
        </template>
      </ElTableColumn>
      <ElTableColumn
        prop="message"
        label="Message"
      />
    </ElTable>
  </div>
</template>
