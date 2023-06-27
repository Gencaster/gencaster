<script setup lang="ts">
import { type Ref, computed, ref } from "vue";

const generateRandom = (min: number, max: number): number => {
  const difference = max - min;
  let rand = Math.random();
  rand = Math.floor(rand * difference);
  rand = rand + min;
  return rand;
};

const barWidth = 4;
const high: number = generateRandom(90, 100) / 100;
const low: number = generateRandom(5, 15) / 100;
const duration: Ref<number> = ref(0.8);
const delay: number = generateRandom(0, 200) / 100;

const cssValue = computed((): string => {
  return `
    width: ${barWidth}px;
    animation-duration: ${duration.value}s;
    animation-delay: -${delay}s;
    --from-hight:${high}; --to-low:${low};
  `;
});
</script>

<template>
  <div
    :style="cssValue"
    class="bar"
  />
</template>

<style lang="scss" scoped>
@import "@/assets/mixins.scss";
@import "@/assets/variables.scss";

.bar {
  background-color: $black;
  height: 100%;
  animation-iteration-count: infinite;
  animation-direction: alternate;
  animation-name: wave;
}

@keyframes wave {
  from {
    transform: scaleY(var(--from-hight));
  }

  to {
    transform: scaleY(var(--to-low));
  }
}
</style>
