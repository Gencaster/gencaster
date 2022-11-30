<template>
  <div class="block">
    <!-- {{ cellData }} -->
    <!-- markdown -->
    <div v-if="editor && editorType === 'markdown'" class="editor-markdown">
      <EditorContent :editor="editor" />
    </div>

    <!-- python -->
    <div v-if="editorType === 'python'" class="editor-python">
      <Codemirror
        v-model="code" placeholder="Code goes here..." :autofocus="false" :indent-with-tab="true"
        :tab-size="2" :extensions="extensions" @ready="codemirrorReady" @change="emitCodemirror('change', $event)"
        @focus="emitCodemirror('focus', $event)" @blur="emitCodemirror('blur', $event)"
      />
    </div>

    <!-- supercollider -->
    <div v-if="editorType === 'supercollider'" class="editor-supercollider">
      <Codemirror
        v-model="code" placeholder="Code goes here..." :autofocus="false" :indent-with-tab="true"
        :tab-size="2" :extensions="extensions" @ready="codemirrorReady" @change="emitCodemirror('change', $event)"
        @focus="emitCodemirror('focus', $event)" @blur="emitCodemirror('blur', $event)"
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
      code: "",
      extensions: undefined
    };
  },

  watch: {},

  mounted() {
    this.editorType = this.cellData.cellType;

    switch (this.editorType) {
      case "comment":
        this.editor = new Editor({
          extensions: [
            StarterKit,
            Highlight,
            Typography
          ],
          content: this.cellData.cellCode,
          // triggered on every change
          onUpdate: () => this.onTipTapUpdate()
        });
        break;

      case "markdown":
        this.editor = new Editor({
          extensions: [
            StarterKit,
            Highlight,
            Typography
          ],
          content: this.cellData.cellCode,
          // triggered on every change
          onUpdate: () => this.onTipTapUpdate()
        });
        break;

      case "python":
        this.code = this.cellData.cellCode;
        this.extensions = [python()];
        break;

      case "supercollider":
        this.code = this.cellData.cellCode;
        this.extensions = [python()];
        break;

      default:
        break;
    }
  },

  beforeUnmount() {
    if (this.editor)
      this.editor.destroy();
  },

  methods: {
    // TipTap
    onTipTapUpdate() {
      // console.log(this.editor.getText());
      // console.log(JSON.stringify(this.editor.getJSON()));
      // console.log(this.editor.getHtml());
    },

    // Python & Supercollider
    emitCodemirror(event, data) {
      // console.log(data);
    },

    codemirrorReady() {
      // console.log("handle ready");
    }
  }
};
</script>

<style lang="scss">
/* Basic editor styles */
</style>
