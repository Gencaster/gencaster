<template>
  <div class="block">
    <!-- {{ cellData }} -->
    <!-- python -->
    <div v-if="editorType === 'python'" class="editor-python">
      <Codemirror
        v-model="code" placeholder="Code goes here..." :style="{ height: '400px' }" :autofocus="true"
        :indent-with-tab="true" :tab-size="2" :extensions="extensions" @ready="handleReady"
        @change="emit('change', $event)" @focus="emit('focus', $event)" @blur="emit('blur', $event)"
      />
    </div>

    <!-- comment -->
    <div v-if="editor && editorType === 'comment'" class="editor-comment">
      <EditorContent :editor="editor" />
    </div>
  </div>
</template>

<script lang="ts">
// python
import { emit } from "process";
import { Codemirror } from "vue-codemirror";
import { python } from "@codemirror/lang-python";

// markdown
import Highlight from "@tiptap/extension-highlight";
import Typography from "@tiptap/extension-typography";
import StarterKit from "@tiptap/starter-kit";
import { Editor, EditorContent } from "@tiptap/vue-3";
// @ts-expect-error: Auto Imported by nuxt
import type { NodeCell } from "~/assets/js/interfaces";
// TODO: Fix typescript import to be linked in editor as well

export default {
  components: {
    EditorContent,
    Codemirror
  },

  props: {
    cellData: {
      type: Object as () => NodeCell,
      required: true,
      default: () => { }
    }
  },

  data() {
    return {
      editorType: "",
      editor: null,
      code: "console.log('Hello, world!')",
      extensions: [python()]
    };
  },

  watch: {},

  mounted() {
    this.editorType = this.cellData.cellType;

    if (this.editorType === "comment") {
      this.editor = new Editor({
        extensions: [
          StarterKit,
          Highlight,
          Typography
        ],
        content: this.cellData.cellCode,
        // triggered on every change
        onUpdate: () => this.onEditorUpdate()
      });
    }
    else if (this.editorType === "python") {
      console.log("python");
    }
  },

  beforeUnmount() {
    this.editor.destroy();
  },

  methods: {
    onEditorUpdate() {
      // console.log(this.editor.getText());
      // console.log(JSON.stringify(this.editor.getJSON()));
      // console.log(this.editor.getHtml());
    },
    emit(event, data) {
      console.log(data);
    },

    handleReady() {
      console.log("handle ready");
    }
  }
};
</script>

<style lang="scss">
/* Basic editor styles */
</style>
