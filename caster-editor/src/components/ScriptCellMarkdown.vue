<template>
  <div class="block block-markdown">
    <div
      :class="{
        'editor-comment': cellType === CellType.Comment,
        'editor-markdown': cellType === CellType.Markdown,
      }"
    >
      <div ref="editorDom" />
    </div>
  </div>
</template>

<script lang="ts" setup>
// Docs : https://github.com/nhn/tui.editor/tree/master/docs/en
// Custom Markdown Commands: https://github.com/nhn/tui.editor/blob/master/docs/en/plugin.md
import "@toast-ui/editor/dist/toastui-editor.css"; // Editor's Style
import Editor from "@toast-ui/editor";
import type { EditorOptions, Editor as EditorType } from "@toast-ui/editor";
import { storeToRefs } from "pinia";
import { CellType } from "@/graphql";
import { computed, onMounted, onUnmounted, ref, type Ref } from "vue";
import { useInterfaceStore } from "@/stores/InterfaceStore";

const props = defineProps<{
  // receiving any updates does not work b/c TUI does not support a v-model binding
  // see https://github.com/nhn/tui.editor/issues/1023
  text: string;
  uuid: string;
  cellType: CellType.Markdown | CellType.Comment;
}>();

const emit = defineEmits<{
  (e: "update:text", text: string): void;
}>();

// Store
const { newScriptCellUpdates } = storeToRefs(useInterfaceStore());

// Variables
const editorDom: Ref<HTMLElement | undefined> = ref();
const editor: Ref<EditorType | undefined> = ref();

const scriptCellText = computed<string>({
  get() {
    return props.text;
  },
  set(value) {
    emit("update:text", value);
    let update = newScriptCellUpdates.value.get(props.uuid);

    if (update) {
      update.cellCode = value;
    } else {
      newScriptCellUpdates.value.set(props.uuid, {
        uuid: props.uuid,
        cellCode: value,
      });
    }
    return value;
  },
});

onMounted(() => {
  const options: EditorOptions = {
    el: editorDom.value as HTMLElement,
    height: "auto",
    initialEditType: "markdown",
    usageStatistics: false,
    initialValue: props.text,
    previewStyle: "tab",
    toolbarItems: [],
    hideModeSwitch: true,
    autofocus: false,
  };

  editor.value = new Editor(options);

  // add events
  editor.value.on("change", () => {
    scriptCellText.value = editor.value?.getMarkdown() || "";
  });
});

onUnmounted(() => {
  if (editor.value) {
    editor.value.destroy();
  }
});
</script>

<style lang="scss" scoped>
@import "@/assets/scss/variables.module.scss";

.editor-comment,
.editor-markdown {
  :deep(.toastui-editor-defaultUI) {
    border: none;
    z-index: 1;

    .toastui-editor {
      min-height: 60px !important;
    }

    // this fixes sortable js
    .toastui-editor-pseudo-clipboard {
      display: none;
    }

    .placeholder {
      .ProseMirror-trailingBreak {
        display: none;
      }
    }
  }

  /* Hiding the nav bar*/
  :deep(.toastui-editor-toolbar) {
    display: none;
  }
}
</style>
