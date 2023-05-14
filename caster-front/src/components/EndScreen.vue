<script setup lang="ts">
import { storeToRefs } from "pinia";
import { usePlayerStore } from "@/stores/Player";
import Content from "@/components/Content.vue";

const { endContent } = storeToRefs(usePlayerStore());
</script>

<template>
  <div class="end-screen">
    <Content :text="endContent" />
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

.end-screen {
  box-sizing: border-box;
  max-width: $desktopMaxWidthText;
  margin: 0 auto;

  padding-bottom: $spacingXL;

  img {
    width: 100%;
  }
}
</style>
