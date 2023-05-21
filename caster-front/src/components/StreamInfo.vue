<script setup lang="ts">
import { ElDescriptions, ElDescriptionsItem } from "element-plus";
import { storeToRefs } from "pinia";
import { usePlayerStore } from "@/stores/Player";
import type { Stream, StreamInstruction, StreamPoint } from "@/graphql";

defineProps<{
  streamInstruction?: null | undefined | Pick<StreamInstruction, "instructionText">
  stream?: Pick<Stream, "uuid"> & {
    streamPoint?: Pick<StreamPoint, "janusInRoom" | "janusOutRoom" | "port">
  }
}>();

const { play, micActive, streamGPS } = storeToRefs(usePlayerStore());
</script>

<template>
  <div class="stream-info">
    <ElDescriptions
      :column="1"
      border
    >
      <ElDescriptionsItem label="Stream UUID">
        {{ stream?.uuid }}
      </ElDescriptionsItem>
      <ElDescriptionsItem label="SuperCollider port">
        {{ stream?.streamPoint?.port }}
      </ElDescriptionsItem>
      <ElDescriptionsItem label="Janus Rooms">
        In: {{ stream?.streamPoint?.janusInRoom }}<br>
        Out: {{ stream?.streamPoint?.janusOutRoom }}
      </ElDescriptionsItem>
      <ElDescriptionsItem label="Local status">
        Playing: {{ play }}<br>
        Mic active: {{ micActive }}<br>
        GPS: {{ streamGPS }}
      </ElDescriptionsItem>
      <ElDescriptionsItem label="Current instruction">
        <span>{{ streamInstruction?.instructionText }}</span>
      </ElDescriptionsItem>
    </ElDescriptions>
  </div>
</template>
