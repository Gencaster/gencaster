<script setup lang="ts">
import { computed } from "vue";
import { ElContainer, ElMain } from "element-plus";
import MarkdownIt from "markdown-it";
import Content from "@/components/Content.vue";

const props = defineProps<{
  text: string
}>();

const description = computed<string>(() => {
  const md = new MarkdownIt();
  return md?.render(props.text);
});
</script>

<template>
  <div>
    <ElContainer class="end-screen">
      <ElMain>
        <Content :text="description" class="content" />
      </ElMain>
    </ElContainer>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/mixins.scss';
@import '@/assets/variables.scss';

.end-screen {
  padding: 0;
  position: relative;
  width: 100%;
  height: auto;
  box-sizing: border-box;
  background-color: $white;
  padding-bottom: $playerBarHeight;

  :deep(img) {
    width: 100%;
  }
}
</style>
