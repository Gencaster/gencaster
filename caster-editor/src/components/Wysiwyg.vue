<!-- eslint-disable vue/no-v-model-argument -->
<script lang="ts" setup>
import { reactive, ref, onMounted, onDeactivated, type Ref } from "vue";

import "@toast-ui/editor/dist/toastui-editor.css"; // Editor's Style
import type { EditorOptions, Editor as EditorType } from "@toast-ui/editor";
import Editor from "@toast-ui/editor";

// props
const props = defineProps<{
  text: string;
}>();

// Editor Settings
const editorDom: Ref<HTMLElement | undefined> = ref();
const editor: Ref<EditorType | undefined> = ref();

onMounted(() => {
  const options: EditorOptions = {
    el: editorDom.value as HTMLElement,
    height: "auto",
    minHeight: "0px",
    initialEditType: "wysiwyg",
    usageStatistics: false,
    initialValue: props.text,
    previewStyle: "tab",
    // https://github.com/nhn/tui.editor/blob/master/docs/en/toolbar.md
    toolbarItems: [
      ["heading", "bold", "italic", "strike"],
      ["hr"],
      ["ul", "ol"],
      ["table", "image", "link"],
    ],
    hideModeSwitch: true,
    autofocus: false,
  };

  console.log(props.text);

  editor.value = new Editor(options);

  // add events
  // editor.value.on("change", () => {
  //   scriptCellText.value = editor.value?.getMarkdown() || "";
  // });
});

onDeactivated(() => {
  if (editor.value) {
    editor.value.destroy();
  }
});
</script>

<template>
  <div class="wysiwyg-wrapper">
    <div
      ref="editorDom"
      class="editor"
    />
  </div>
</template>

<style lang="scss" scoped>
@import "@/assets/scss/variables.module.scss";

.wysiwyg-wrapper {
  width: 100%;
  margin: 0 !important;
}

.editor {
  position: relative;
  display: block;
  width: 100%;

  :deep(.toastui-editor-defaultUI-toolbar) {
    background-color: $grey-light !important;
  }
}
</style>
