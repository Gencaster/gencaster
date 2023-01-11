<script setup lang="ts">
import { storeToRefs } from "pinia";
import { ref } from "vue";
import { useStreamPointStore } from "@/stores/StreamPoints";

const props = defineProps<{
  uuid: String
}>();

const { streamPoints, activeStreamPoint } = storeToRefs(useStreamPointStore());

const streamPoint = ref(streamPoints.value.find(x => x.uuid === props.uuid));

const setActive = () => {
  if (streamPoint.value !== undefined)
    activeStreamPoint.value = streamPoint.value;
};
</script>

<template>
  <h3 @click="() => { setActive() }">
    Stream Point {{ streamPoint?.port }}
  </h3>
</template>
