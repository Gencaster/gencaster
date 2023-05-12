<script setup lang="ts">
import { computed, onMounted } from "vue";

import { storeToRefs } from "pinia";
import { usePlayerStore } from "@/stores/Player";
const { userDataRequests } = storeToRefs(usePlayerStore());

const popupToShow = computed(() => {
  if (userDataRequests.value.length > 0)
    return userDataRequests.value[userDataRequests.value.length - 1];
  else
    return null;
});

onMounted(() => {
  const testPopup = {
    name: "Name",
    description: "Bitte teile uns deinen Namen mit.",
    key: "username",
    type: "string",
    placeholder: "Name Placeholder"
  };

  userDataRequests.value.push(testPopup);
});
</script>

<template>
  <div>
    <div class="wrapper fullscreen-wrapper-fixed" />
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

.wrapper {

  background-color: yellow;
}
</style>
