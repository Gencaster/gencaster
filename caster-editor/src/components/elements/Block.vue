<template>
  <div class="block">
    {{ code }}
    <!-- markdown -->
    <div v-if="editor && editorType === CellType.Markdown" class="editor-markdown">
      <EditorContent :editor="editor" />
    </div>

    <!-- python -->
    <div v-if="editorType === CellType.Python" class="editor-python">
      <Codemirror
        v-model="code" placeholder="Code goes here..." :autofocus="false" :indent-with-tab="true"
        :tab-size="2" :extensions="extensions" @ready="codemirrorReady" @change="emitCodemirror('change', $event)"
        @focus="emitCodemirror('focus', $event)" @blur="emitCodemirror('blur', $event)"
      />
    </div>

    <!-- supercollider -->
    <div v-if="editorType === CellType.Supercollider" class="editor-supercollider">
      <Codemirror
        v-model="code" placeholder="Code goes here..." :autofocus="false" :indent-with-tab="true"
        :tab-size="2" :extensions="extensions" @ready="codemirrorReady" @change="emitCodemirror('change', $event)"
        @focus="emitCodemirror('focus', $event)" @blur="emitCodemirror('blur', $event)"
      />
    </div>

    <!-- comment -->
    <div v-if="editor && editorType === CellType.Comment" class="editor-comment">
      <EditorContent :editor="editor" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { Codemirror } from "vue-codemirror";
import { python } from "@codemirror/lang-python";

// markdown
import Highlight from "@tiptap/extension-highlight";
import Typography from "@tiptap/extension-typography";
import StarterKit from "@tiptap/starter-kit";
import { Editor, EditorContent } from "@tiptap/vue-3";
import { CellType } from "@/graphql/graphql";
import type { ScriptCell } from "@/graphql/graphql";

interface BlockProps {
  cellData: ScriptCell
}

const props = defineProps<BlockProps>();

// Variables
const editorType = ref<string>();
let editor = ref<any>({});
const code = ref<string>();
let extensions = ref<any>([]);

// methods
const onTipTapUpdate = () => {
  console.log(editor.getText());
  console.log(JSON.stringify(editor.getJSON()));
  console.log(editor.getHtml());
};

const emitCodemirror = (eventType?: string, event?: any) => {};
const codemirrorReady = () => {};
// onTipTapUpdate() {
// // console.log(this.editor.getText());
// // console.log(JSON.stringify(this.editor.getJSON()));
// // console.log(this.editor.getHtml());
//     },

editorType.value = props.cellData.cellType;

switch (editorType.value) {
  case CellType.Comment:
    editor = new Editor({
      extensions: [
        StarterKit,
        Highlight,
        Typography
      ],
      content: props.cellData.cellCode,
      // triggered on every change
      onUpdate: () => onTipTapUpdate()
    });
    break;

  case CellType.Markdown:
    editor = new Editor({
      extensions: [
        StarterKit,
        Highlight,
        Typography
      ],
      content: props.cellData.cellCode,
      // triggered on every change
      onUpdate: () => onTipTapUpdate()
    });
    break;

  case CellType.Python:
    code.value = props.cellData.cellCode;
    extensions = [python()];
    break;

  case CellType.Supercollider:
    code.value = props.cellData.cellCode;
    extensions = [python()];
    break;

  default:
    break;
}
</script>
