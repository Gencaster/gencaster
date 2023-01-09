<script setup lang="ts">
import { storeToRefs } from "pinia";
import StreamPoint from "./StreamPoint.vue";
import { useStreamPointStore } from "@/stores/StreamPoints";

const { streamPoints } = storeToRefs(useStreamPointStore());
</script>

<template>
  <h2>Stream Points</h2>
  <ul>
    <li v-for="streamPoint in streamPoints" :key="streamPoint.uuid">
      <StreamPoint
        :uuid="streamPoint.uuid"
      />
    </li>
  </ul>
</template>
