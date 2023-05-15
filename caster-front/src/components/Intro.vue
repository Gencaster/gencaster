<script setup lang="ts">
import { storeToRefs } from "pinia";
import { ElButton, ElCard } from "element-plus";
import { usePlayerStore } from "@/stores/Player";
import { PlayerState } from "@/models";
import GraphPlayerCredits from "@/components/GraphPlayerCredits.vue";
const {
  title,
  startingTimestamp,
  description,
  playerState,
  play
} = storeToRefs(usePlayerStore());

const startListening = () => {
  play.value = true;
  playerState.value = PlayerState.Playing;
  startingTimestamp.value = new Date().getTime();
};
</script>

<template>
  <div class="fullscreen-wrapper-relative">
    <ElCard class="title-card">
      <template #header>
        <div class="card-header">
          <h1 class="title">
            {{ title }}
          </h1>
        </div>
      </template>
      <p class="description">
        {{ description }}
      </p>
      <div class="button-wrapper">
        <ElButton class="caps green" size="large" type="default" @click="startListening()">
          Start
        </ElButton>
      </div>
    </ElCard>
    <GraphPlayerCredits />
  </div>
</template>

<style lang="scss" scoped>

</style>
