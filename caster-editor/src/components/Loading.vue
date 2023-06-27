<template>
  <div class="fetching-screen">
    <p>Loading...</p>
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/scss/variables.module.scss";

.fetching-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: $bodyBackground;
  padding: 5px 12px 5px 12px;
  display: flex;
  z-index: 99;
}
</style>
