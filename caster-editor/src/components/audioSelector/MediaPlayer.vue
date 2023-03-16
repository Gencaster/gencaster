<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { AudioFile } from "@/graphql";

export interface MediaPlayerProps {
  audio: AudioFile;
}

const audioplayer = ref<HTMLAudioElement | null>(null)
const audioPlaying = ref(false)

defineProps<MediaPlayerProps>();


const toggleAudio = () => {
  if (audioplayer.value === null) return

  if (audioPlaying.value) {
    audioPlaying.value = false
    audioplayer.value.pause()
    audioplayer.value.currentTime = 0;
  } else {
    audioPlaying.value = true
    audioplayer.value.play()
  }
}

onMounted(() => {
  audioplayer.value?.addEventListener('ended', () => {
    audioPlaying.value = false
  })
})

</script>

<template>
  <div class="media-player">
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
    <p>{{ audio.name || 'no name' }}</p>
    <p>{{ audio.lastUpdate || 'no date' }}</p>

    <audio
      ref="audioplayer"
      :src="`http://127.0.0.1:8081${audio.file.url}`"
    />
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/scss/variables.module.scss';

.media-player {
  display: flex;
  height: 26px;
  width: 100%;
  align-items: center;

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
    transform: translateX(-1px);
  }
}
</style>
