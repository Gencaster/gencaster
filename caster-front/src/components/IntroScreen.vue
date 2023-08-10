<script setup lang="ts">
import { ElButton, ElCard } from "element-plus";
import MarkdownIt from "markdown-it";
import { computed } from "vue";

const props = defineProps<{
  title: string;
  descriptionText: string;
  buttonText: string;
  moreInfo: boolean;
}>();

const emit = defineEmits<{
  (e: "buttonClicked"): void;
}>();

const description = computed<string>(() => {
  const md = new MarkdownIt();
  return md?.render(props.descriptionText);
});
</script>

<template>
  <!-- eslint-disable vue/no-v-html -->
  <div class="fullscreen-wrapper-relative">
    <ElCard class="title-card">
      <template #header>
        <div class="card-header">
          <h1 class="title">
            {{ title }}
          </h1>
        </div>
      </template>
      <p
        class="description"
        v-html="description"
      />
      <div class="button-wrapper">
        <ElButton
          class="caps green"
          size="large"
          type="default"
          @click="emit('buttonClicked')"
        >
          {{ buttonText }}
        </ElButton>
      </div>
    </ElCard>
    <div class="credits">
      <p>
        made with <a
          href="https://gencaster.org/"
          target="_blank"
        >gencaster</a>
        <span v-if="moreInfo"> - more info ↓</span>
      </p>
      <p />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/mixins.scss";
@import "@/assets/variables.scss";

.credits {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;

  p {
    text-align: center;
  }
}
</style>
