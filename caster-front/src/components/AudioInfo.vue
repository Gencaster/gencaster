<script setup lang="ts">
import { storeToRefs } from "pinia";
import { ElButton, ElContainer, ElHeader, ElMain } from "element-plus";
import { usePlayerStore } from "@/stores/Player";
import Content from "@/components/Content.vue";

const { infoContent, showInfo } = storeToRefs(usePlayerStore());
</script>

<template>
  <div>
    <ElContainer class="info-screen">
      <ElHeader class="header">
        <ElButton class="caps" size="default" text @click="showInfo = false">
          <span>
            Schließen
          </span>
        </ElButton>
      </ElHeader>
      <ElMain>
        <Content :text="infoContent" class="content" />
      </ElMain>
    </ElContainer>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

.info-screen {
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

.content {
  width: calc(100% - 2 * $mobilePadding);
  margin-top: 0;
  padding-top: $playerBarHeight;
  margin-bottom: $spacingM;
}

:deep(.text) > :first-child {
  margin-top: 0;
}

.header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  background-color: $white;
}
</style>
