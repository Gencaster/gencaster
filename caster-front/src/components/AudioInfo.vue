<script setup lang="ts">
import { computed } from "vue";
import { ElButton, ElContainer, ElHeader, ElMain } from "element-plus";
import MarkdownIt from "markdown-it";
import Content from "@/components/ContentParser.vue";

const props = defineProps<{
  text: string;
}>();

const emit = defineEmits<{
  (e: "clicked-close"): void;
}>();

const description = computed<string>(() => {
  const md = new MarkdownIt();
  return md?.render(props.text);
});
</script>

<template>
  <div>
    <ElContainer class="info-screen">
      <ElHeader class="header">
        <ElButton
          class="caps"
          size="default"
          text
          @click="emit('clicked-close')"
        >
          <span> Schließen </span>
        </ElButton>
      </ElHeader>
      <ElMain>
        <Content
          :text="description"
          class="content"
        />
      </ElMain>
    </ElContainer>
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/mixins.scss";
@import "@/assets/variables.scss";

.info-screen {
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

.content {
  width: calc(100% - 2 * $mobilePadding);
  margin-top: 0;
  padding-top: $playerBarHeight;
  margin-bottom: $spacingM;
}

:deep(.text) > :first-child {
  margin-top: 0;
}

.header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  background-color: $white;
}
</style>
