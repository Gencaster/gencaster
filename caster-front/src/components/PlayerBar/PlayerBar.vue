<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import { storeToRefs } from "pinia";
import { usePlayerStore } from "@/stores/Player";
defineProps<{
  title: string
}>();

const { startingTimestamp, play, playerState, showInfo } = storeToRefs(usePlayerStore());

const format = (num: number) => {
  const s = `${num}`;
  return s.length <= 1 ? `0${s}` : s;
};

const duration = ref("00:00");

let interval: number;

const stopInterval = () => {
  if (window && interval)
    window.clearInterval(interval);
};

const initInterval = () => {
  interval = window.setInterval(() => {
    if (playerState.value === "end" && stopInterval) {
      stopInterval();
      return;
    }

    const now = new Date();
    const diff = now.getTime() - startingTimestamp.value;
    const minutes = Math.floor(diff / 60000);
    const seconds = Math.floor((diff - minutes * 60000) / 1000);
    duration.value = `${format(minutes)}:${format(seconds)}`;
  }, 1000);
};

const stopPlayer = () => {
  play.value = false;
  playerState.value = "end";
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
    <h1 v-if="playerState !== 'end'" class="title">
      {{ title }}
    </h1>
    <div class="player-bar">
      <div class="element">
        <button class="text-btn text-btn-medium" @click="showInfo = true">
          <span>INFO</span>
        </button>
      </div>
      <div class="element time">
        <span>{{ duration }}</span>
      </div>
      <div class="element">
        <button class="text-btn text-btn-medium" @click="stopPlayer()">
          <div v-if="playerState !== 'end'" class="stop-icon" />
          <Transition>
            <span v-if="playerState === 'end'" />
            <span v-else>STOP</span>
          </Transition>
        </button>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

.title {
  margin: 0;
  padding: 0;
  position: fixed;
  bottom: 50px;
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
  height: 50px;
  width: 100%;
  padding-left: $mobilePadding;
  padding-right: $mobilePadding;
  ;

  border-top: $lineStandard solid $black;

  display: flex;
  justify-content: space-between;
  align-items: center;

  background: $white;

  font-size: $mediumFontSize;

  .element {
    width: 32%;
    display: flex;
    justify-content: center;
  }

  .element:first-child {
    justify-content: flex-start;
  }

  .element:last-child {
    justify-content: flex-end;
  }
}

.time {
  font-variant-numeric: tabular-nums;
}

.stop-icon {
  width: 18px;
  height: 18px;
  background-color: $black;
  border-radius: $borderRadius;
  transform: translateY(-1px);
}
</style>
