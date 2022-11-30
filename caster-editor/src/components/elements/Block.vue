<template>
  <div>
    {{ cellData }}
    <EditorContent :editor="editor" />
  </div>
</template>

<script lang="ts">
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
      default: () => {}
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

    this.editor = new Editor({
      extensions: [
        StarterKit
      ],
      content: `
        <h2>
          Hi there,
        </h2>
        <p>
          this is a <em>basic</em> example of <strong>tiptap</strong>. Sure, there are all kind of basic text styles you’d probably expect from a text editor. But wait until you see the lists:
        </p>
      `
    });
  },

  beforeUnmount() {
    this.editor.destroy();
  }
};
</script>

<style lang="scss">
/* Basic editor styles */
.ProseMirror {
  > * + * {
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
    font-family: 'JetBrainsMono', monospace;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;

    code {
      color: inherit;
      padding: 0;
      background: none;
      font-size: 0.8rem;
    }
  }

  img {
    max-width: 100%;
    height: auto;
  }

  blockquote {
    padding-left: 1rem;
    border-left: 2px solid rgba(#0D0D0D, 0.1);
  }

  hr {
    border: none;
    border-top: 2px solid rgba(#0D0D0D, 0.1);
    margin: 2rem 0;
  }
}
</style>
