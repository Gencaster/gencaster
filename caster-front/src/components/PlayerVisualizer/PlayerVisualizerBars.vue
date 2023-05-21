<script setup lang="ts">
import { onMounted, ref } from "vue";
import Bar from "@/components/PlayerVisualizer/PlayerVisualizerBar.vue";

const wrapper = ref<HTMLDivElement>();
const numberOfBars = ref<number>(20);
const distanceBars = ref<number>(22);

const setBars = (): void => {
  const width = wrapper.value?.clientWidth || 0;
  const amount = Math.floor(width / distanceBars.value);
  numberOfBars.value = amount;
};

const resizeObserver: ResizeObserver = new ResizeObserver(() => {
  setBars();
});

onMounted(() => {
  setBars();
  if (wrapper.value)
    resizeObserver.observe(wrapper.value);
});
</script>

<template>
  <div ref="wrapper" class="bars-wrapper">
    <div v-for="(index) in numberOfBars" :key="index" class="bar-wrapper">
      <Bar />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

.bars-wrapper {
  width: 100%;
  height: 100%;

  display: flex;
  justify-content: space-between;
}
</style>
