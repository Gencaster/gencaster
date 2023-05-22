<script setup lang="ts"></script>

<template>
  <div class="credits">
    <p>
      made with <a
        href="https://gencaster.org/"
        target="_blank"
      >gencaster</a>
    </p>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

.credits {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;

  p {
    text-align: center;
  }
}
</style>
