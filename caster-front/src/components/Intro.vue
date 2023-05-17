<script setup lang="ts">
import { ElButton, ElCard } from "element-plus";
import MarkdownIt from "markdown-it";
import { computed } from "vue";
import GraphPlayerCredits from "@/components/GraphPlayerCredits.vue";

const props = defineProps<{
  title: string
  descriptionText: string
  buttonText: string
}>();

const emit = defineEmits<{
  (e: "buttonClicked"): void
}>();

const description = computed<string>(() => {
  const md = new MarkdownIt();
  return md?.render(props.descriptionText);
});
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
      <p class="description" v-html="description" />
      <div class="button-wrapper">
        <ElButton class="caps green" size="large" type="default" @click="emit('buttonClicked')">
          {{ buttonText }}
        </ElButton>
      </div>
    </ElCard>
    <GraphPlayerCredits />
  </div>
</template>

<style lang="scss" scoped>

</style>
