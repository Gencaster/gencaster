<script lang="ts" setup>
import { ref, onMounted, type Ref } from "vue";
import type { AudioFile, DjangoFileType } from "@/graphql";

export interface AudioType extends Pick<AudioFile, 'name'> {
  file: Pick<DjangoFileType, 'url'>
}

export interface AudioFilePlayerProps {
  audioFile:  AudioType;
}

const audioPlayer: Ref<HTMLAudioElement | undefined> = ref()
const audioPlaying = ref(false)

defineProps<AudioFilePlayerProps>();


const toggleAudio = () => {
  if (audioPlayer.value === null) return

  if (audioPlaying.value) {
    audioPlaying.value = false
    if(audioPlayer.value) {
      audioPlayer.value.pause()
      audioPlayer.value.currentTime = 0;
    }
  } else {
    audioPlaying.value = true
    if(audioPlayer.value) {
      audioPlayer.value.play()
    }
  }
}

onMounted(() => {
  audioPlayer.value?.addEventListener('ended', () => {
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
    <p>{{ audioFile.name }}</p>
    <p>no date</p>

    <audio
      v-if="audioFile.file"
      ref="audioPlayer"
      :src="`http://127.0.0.1:8081${audioFile.file.url}`"
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
    transform: translateX(0px);
  }
}
</style>
