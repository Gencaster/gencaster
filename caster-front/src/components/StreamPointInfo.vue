<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { ElDescriptions, ElDescriptionsItem } from "element-plus";
import { usePlayerStore } from "@/stores/Player";

const { activeStreamPoint } = storeToRefs(usePlayerStore());
</script>

<template>
  <ElDescriptions title="Stream information">
    <ElDescriptionsItem label="StreamPoint port">
      {{ activeStreamPoint?.port }}
    </ElDescriptionsItem>
    <ElDescriptionsItem label="Janus In Port">
      {{ activeStreamPoint?.janusInPort }}
    </ElDescriptionsItem>
    <ElDescriptionsItem label="Janus Out Port">
      {{ activeStreamPoint?.janusOutPort }}
    </ElDescriptionsItem>
    <ElDescriptionsItem label="Janus In Room">
      {{ activeStreamPoint?.janusInRoom }}
    </ElDescriptionsItem>
    <ElDescriptionsItem label="Janus Out Room">
      {{ activeStreamPoint?.janusOutRoom }}
    </ElDescriptionsItem>
    <ElDescriptionsItem label="UUID">
      {{ activeStreamPoint?.uuid }}
    </ElDescriptionsItem>
  </ElDescriptions>
</template>
