<script setup lang="ts">
defineProps({
  text: String
});
</script>

<template>
  <div class="info-popup">
    <div class="text" v-html="text" />
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

.content-screen {
  box-sizing: border-box;
  max-width: $desktopMaxWidthText;
  margin: 0 auto;

  :deep(img) {
    width: 100%;
  }
}
</style>
