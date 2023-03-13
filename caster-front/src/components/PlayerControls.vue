<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { usePlayerStore } from "@/stores/Player";
import GpsStreaming from "@/components/GpsStreaming.vue";

const { play, micActive } = storeToRefs(usePlayerStore());
</script>

<template>
  <div>
    <el-button
      class="button"
      type="primary"
      @click="play = true"
    >
      Start
    </el-button>
    <el-button
      class="button"
      type="danger"
      @click="() => play = false"
    >
      Stop
    </el-button>
    <el-button
      class="button"
      type="warning"
      @click="() => micActive = !micActive"
    >
      {{ micActive ? "Disable" : "Activate" }} mic
    </el-button>
    <GpsStreaming />
  </div>
</template>
