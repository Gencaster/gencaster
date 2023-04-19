<script setup lang="ts">
import { ElButton, ElCollapse, ElCollapseItem } from "element-plus";
import { type Ref, ref } from "vue";
import StreamInfo from "./StreamInfo.vue";
import StreamPoints from "@/components/StreamPoints.vue";
import type { StreamPoint } from "@/graphql";
import PlayerButtons from "@/components/PlayerButtons.vue";
import Player from "@/components/Player.vue";

const selectedStreamPoint: Ref<StreamPoint | undefined> = ref();
</script>

<template>
  <div class="debug-player">
    <h4>Debug Player</h4>

    <ElCollapse>
      <ElCollapseItem title="Streaming points">
        <StreamPoints
          @selected-stream-point="(streamPoint) => selectedStreamPoint = streamPoint"
        />
        <ElButton
          style="width: 100%; margin-top: 10px;"
          @click="selectedStreamPoint = undefined"
        >
          Reset streaming point
        </ElButton>
      </ElCollapseItem>
      <ElCollapseItem title="Player">
        <div v-if="selectedStreamPoint">
          <PlayerButtons />
          <Player
            :stream-point="selectedStreamPoint"
          />
        </div>
        <div v-else>
          Please select a streaming point first
        </div>
      </ElCollapseItem>
      <ElCollapseItem title="Debug info">
        <div v-if="selectedStreamPoint">
          <StreamInfo
            :stream="{ uuid: 'none', streamPoint: selectedStreamPoint }"
          />
        </div>
        <div v-else>
          <span>No stream selected</span>
        </div>
      </ElCollapseItem>
    </ElCollapse>
  </div>
</template>
