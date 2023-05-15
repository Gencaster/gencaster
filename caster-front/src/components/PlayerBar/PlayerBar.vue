<script setup lang="ts">
import { type Ref, computed, onBeforeUnmount, onMounted, ref } from "vue";
import { ElButton, ElCol, ElRow } from "element-plus";
import { storeToRefs } from "pinia";
import { usePlayerStore } from "@/stores/Player";
import { PlayerState } from "@/models";

const { startingTimestamp, play, playerState, showInfo, title } = storeToRefs(usePlayerStore());

const format = (num: number): string => {
  return num.toString().padStart(2, "0");
};

let interval: number;
const duration: Ref<number> = ref(0);

const stopInterval: VoidFunction = () => {
  if (window && interval)
    window.clearInterval(interval);
};

const initInterval: VoidFunction = () => {
  interval = window.setInterval(() => {
    if (playerState.value === PlayerState.End) {
      stopInterval();
      return;
    }

    const now = new Date();
    const diff = now.getTime() - startingTimestamp.value;
    duration.value = diff;
  }, 1000);
};

const minutesSinceStart = computed<string>(() => {
  const minutes = Math.floor(duration.value / 60000);
  return format(minutes).toString();
});

const secondsSinceStart = computed<string>(() => {
  const minutes = Math.floor(duration.value / 60000);
  const seconds = Math.floor((duration.value - minutes * 60000) / 1000);
  return format(seconds).toString();
});

const stopPlayer: VoidFunction = () => {
  play.value = false;
  playerState.value = PlayerState.End;
};

onMounted(() => {
  initInterval();
});

onBeforeUnmount(() => {
  stopInterval();
});
</script>

<template>
  <div>
    <h1 v-if="playerState !== PlayerState.End" class="title general-padding">
      {{ title }}
    </h1>
    <ElRow class="player-bar general-padding">
      <ElCol :span="8">
        <ElButton class="caps" size="default" text @click="showInfo = !showInfo">
          <span>
            Info
          </span>
        </ElButton>
      </ElCol>
      <ElCol class="tabular-nums" :span="8">
        <span>{{ minutesSinceStart }}:{{ secondsSinceStart }}</span>
      </ElCol>
      <ElCol :span="8">
        <ElButton class="caps" size="default" text @click="stopPlayer()">
          <div v-if="playerState !== PlayerState.End" class="stop-icon" />
          <Transition>
            <span v-if="playerState === PlayerState.End" />
            <span v-else>STOP</span>
          </Transition>
        </ElButton>
      </ElCol>
    </ElRow>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

.title {
  margin: 0;
  padding-top: 0;
  padding-bottom: 0;
  position: fixed;
  bottom: $playerBarHeight;
  max-width: 50%;
  margin-bottom: 8px;
  line-height: 1.2;

  @include onScreen('phone-only') {
    max-width: 100%;
  }

}

.player-bar {
  z-index: 10;
  box-sizing: border-box;
  position: fixed;
  bottom: 0;
  left: 0;
  height: $playerBarHeight;
  width: 100%;
  justify-content: space-between;
  align-items: center;
  border-top: $lineStandard solid $black;
  background: $white;
  font-size: $mediumFontSize;

  .el-col {
    display: flex;
    justify-content: center;
  }

  .el-col:first-child {
    justify-content: flex-start;
  }

  .el-col:last-child {
    justify-content: flex-end;
  }

  .stop-icon {
  width: 18px;
  height: 18px;
  background-color: $black;
  border-radius: $borderRadius;
  transform: translateY(-1px);
  margin-right: 4px;
}
}
</style>
