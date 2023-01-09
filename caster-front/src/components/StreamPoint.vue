<script setup lang="ts">
import { storeToRefs } from "pinia";
import { ref } from "vue";
import { useStreamPointStore } from "@/stores/StreamPoints";

const props = defineProps<{
  uuid: String
}>();

const { streamPoints } = storeToRefs(useStreamPointStore());

const streamPoint = ref(streamPoints.value.find(x => x.uuid === props.uuid));
</script>

<template>
  <h3>Stream Point {{ streamPoint?.port }}</h3>
</template>
