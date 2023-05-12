<script setup lang="ts">
import { storeToRefs } from "pinia";
import { usePlayerStore } from "@/stores/Player";
import Content from "@/components/Content.vue";

const { infoContent, showInfo } = storeToRefs(usePlayerStore());
</script>

<template>
  <div class="fullscreen-wrapper-fixed">
    <div class="info-screen">
      <div class="header">
        <button class="caps underline text-btn text-btn-medium" @click="showInfo = false">
          <span>Schließen</span>
        </button>
      </div>
      <Content :text="infoContent" class="content" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

.fullscreen-wrapper-fixed {
  z-index: 11;
  background-color: $white;
  padding: 0;
}

.info-screen {
  transform: scale(1);
  width: 100%;
  height: 100%;
  overflow-y: scroll;
  box-sizing: border-box;
  // max-width: $desktopMaxWidthText;
  // margin: 0 auto;
  // height: auto;

  :deep(img) {
    width: 100%;
  }
}

.content {
  width: calc(100% - 2 * $mobilePadding);
  margin-top: 0;
  margin-bottom: $spacingL;
}

.content> :first-child {
  margin-top: 0;
  // background-color: yellow;
}

.header {
  width: 100%;
  box-sizing: border-box;
  display: flex;
  justify-content: flex-end;
  margin-top: $spacingM;
  padding-left: $mobilePadding ;
  padding-right: $mobilePadding;
}
</style>
