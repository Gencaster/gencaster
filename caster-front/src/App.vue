<script setup lang="ts">
import { RouterView, useRouter } from "vue-router";
import { ElContainer, ElHeader, ElMain } from "element-plus";

const router = useRouter();
</script>

<template>
  <ElContainer style="max-width: 1000px; margin: 10px auto;">
    <ElHeader>
      <span
        class="text-extra-large font-300 mr-3"
        style="padding: 10px; background-color: greenyellow;"
        @click="router.push({ name: 'home' })"
      >Gencaster</span>
    </ElHeader>
    <ElMain>
      <RouterView />
    </ElMain>
  </ElContainer>
</template>
