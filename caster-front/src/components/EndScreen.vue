<script setup lang="ts">
import { storeToRefs } from "pinia";
import { ElContainer, ElMain } from "element-plus";
import { usePlayerStore } from "@/stores/Player";
import Content from "@/components/Content.vue";

const { endContent } = storeToRefs(usePlayerStore());
</script>

<template>
  <div>
    <ElContainer class="end-screen">
      <ElMain>
        <Content :text="endContent" class="content" />
      </ElMain>
    </ElContainer>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

.end-screen {
  padding: 0;
  position: relative;
  width: 100%;
  height: auto;
  box-sizing: border-box;
  background-color: $white;
  padding-bottom: $playerBarHeight;

  :deep(img) {
    width: 100%;
  }
}
</style>
