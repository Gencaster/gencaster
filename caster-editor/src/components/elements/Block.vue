<template>
  <div>
    <!-- {{ cellData }} -->
    <!-- python -->
    <div v-if="editorType === 'python'" class="editor-python">
      <input type="text">
    </div>

    <!-- comment -->
    <div v-if="editor && editorType === 'comment'" class="editor-comment">
      <EditorContent :editor="editor" />
    </div>
  </div>
</template>

<script lang="ts">
import Highlight from "@tiptap/extension-highlight";
import Typography from "@tiptap/extension-typography";
import StarterKit from "@tiptap/starter-kit";
import { Editor, EditorContent } from "@tiptap/vue-3";
// @ts-expect-error: Auto Imported by nuxt
import type { NodeCell } from "~/assets/js/interfaces";
// TODO: Fix typescript import to be linked in editor as well

export default {
  components: {
    EditorContent
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
      editor: null
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
  },

  beforeUnmount() {
    this.editor.destroy();
  },

  methods: {
    onEditorUpdate() {
      // console.log(this.editor.getText());
      // console.log(JSON.stringify(this.editor.getJSON()));
      // console.log(this.editor.getHtml());
    }
  }
};
</script>

<style lang="scss">
/* Basic editor styles */
.ProseMirror {
  >*+* {
    margin-top: 0.75em;
  }

  ul,
  ol {
    padding: 0 1rem;
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    line-height: 1.1;
  }

  code {
    background-color: rgba(#616161, 0.1);
    color: #616161;
  }

  pre {
    background: #0D0D0D;
    color: #FFF;
    font-family: monospace;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;

    code {
      color: inherit;
      padding: 0;
      background: none;
      font-size: 0.8rem;
    }
  }
}
</style>
