<script lang="ts" setup>
import { watch, ref, onMounted, computed, type Ref } from "vue";
import type { AudioFile, DjangoFileType } from "@/graphql";
import { ElSlider } from "element-plus";

const audioPlayer: Ref<HTMLAudioElement | undefined> = ref();
const audioPlaying = ref(false);
const position: Ref<number> = ref(0.0);

const props = defineProps<{
  audioFile: Pick<AudioFile, 'name'> & {
    createdDate?: string
    file?: undefined | null | Pick<DjangoFileType, 'url'>
  };
  type: 'minimal' | 'browser';
  volume?: number;
}>();

const baseURL: string = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8081";

const toggleAudio = () => {
  if (audioPlayer.value === null) return;

  if (audioPlaying.value) {
    audioPlaying.value = false;
    if (audioPlayer.value) {
      audioPlayer.value.pause();
      audioPlayer.value.currentTime = 0;
    }
  } else {
    audioPlaying.value = true;
    if (audioPlayer.value) {
      audioPlayer.value.play();
    }
  }
};

const normalizedVolume = computed(() => {
  if (props.volume !== undefined && props.volume <= 1 && props.volume >= 0) {
    return props.volume;
  } else {
    return 1;
  }
});

watch(normalizedVolume, () => {
  setVolume();
});

const updatePosition = () => {
  position.value = ((audioPlayer.value?.currentTime ?? 0.0) / (audioPlayer.value?.duration ?? 1.0));
};

const setVolume = () => {
  if (audioPlayer.value === undefined) return;
  audioPlayer.value.volume = normalizedVolume.value;
};

onMounted(() => {
  audioPlayer.value?.addEventListener('ended', () => {
    audioPlaying.value = false;
  });

  setVolume();
});

</script>

<template>
  <div class="media-player">
    <div v-if="type === 'browser'">
      <button @click="toggleAudio">
        <img
          v-if="!audioPlaying"
          src="@/assets/icons/icon-triangle-right.svg"
          alt="Play button"
          class="fixArrow"
        >
        <img
          v-else
          src="@/assets/icons/icon-pause.svg"
          alt="Play button"
        >
      </button>
      <audio
        v-if="audioFile.file"
        ref="audioPlayer"
        :src="`${baseURL}${audioFile.file.url}`"
      />
    </div>
    <div
      v-if="type === 'minimal'"
      class="minimal"
    >
      <button @click="toggleAudio">
        <img
          v-if="!audioPlaying"
          src="@/assets/icons/icon-triangle-right.svg"
          alt="Play button"
          class="fixArrow"
        >
        <img
          v-else
          src="@/assets/icons/icon-pause.svg"
          alt="Play button"
        >
      </button>
      <audio
        v-if="audioFile.file"
        ref="audioPlayer"
        :src="`${baseURL}${audioFile.file.url}`"
        @timeupdate="updatePosition()"
      />
      <ElSlider
        v-model="position"
        :min="0.0"
        :max="1.0"
      />
      <p v-if="audioPlayer">
        {{ (position * (audioPlayer?.duration)).toFixed(0) ?? '' }}s / {{ (audioPlayer?.duration).toFixed(0) ?? '' }}s
      </p>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/scss/variables.module.scss';

.media-player {
  display: flex;
  height: 26px;

  div {
    align-items: center;
    display: flex;
    height: 26px;
  }

  p {
    margin: 0;
    margin-right: 16px;
  }
}

button {
  all: unset;
  cursor: pointer;
  width: 26px;
  height: 26px;
  background: $grey-medium;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;

  img {
    height: 16px;
    width: 16px;
    pointer-events: none;
  }

  .fixArrow {
    transform: translateX(0px);
  }
}

.minimal {

  .el-slider {
    width: 100px;
    margin-right: 16px;
  }
}
</style>
