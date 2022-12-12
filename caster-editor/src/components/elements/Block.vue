<template>
  <div class="block">
    <!-- markdown -->
    <div v-if="editorType === CellType.Markdown" class="editor-markdown">
      <div ref="editorDom" />
    </div>

    <!-- comment -->
    <div v-if="editorType === CellType.Comment" class="editor-comment">
      <div ref="editorDom" />
    </div>

    <!-- python -->
    <div v-if="editorType === CellType.Python" class="editor-python">
      <Codemirror
        v-model="codemirrorCode" placeholder="Code goes here..." :autofocus="false" :indent-with-tab="true"
        :tab-size="2" :extensions="extensions" @ready="codemirrorReady" @change="emitCodemirror('change', $event)"
        @focus="emitCodemirror('focus', $event)" @blur="emitCodemirror('blur', $event)"
      />
    </div>

    <!-- supercollider -->
    <div v-if="editorType === CellType.Supercollider" class="editor-supercollider">
      <Codemirror
        v-model="codemirrorCode" placeholder="Code goes here..." :autofocus="false" :indent-with-tab="true"
        :tab-size="2" :extensions="extensions" @ready="codemirrorReady" @change="emitCodemirror('change', $event)"
        @focus="emitCodemirror('focus', $event)" @blur="emitCodemirror('blur', $event)"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
// code editor
import { Codemirror } from "vue-codemirror";
import { python } from "@codemirror/lang-python";

// markdown editor
import EditorJS from "@editorjs/editorjs";
import Header from "@editorjs/header"; // TODO: Fix Could not find a declaration file for module '@editorjs/header'.
import { CellType } from "@/graphql/graphql";
import type { ScriptCell } from "@/graphql/graphql";

const props = defineProps<BlockProps>();

interface BlockProps {
  cellData: ScriptCell
}

// Variables
const editorType = ref<string>(props.cellData.cellType);
const codemirrorCode = ref<string>();
const extensions = ref<any>([]);
const editorJS = ref<EditorJS>();
const editorDom = ref<HTMLElement>();
const editorJSdata = ref<Object>();

// methods
const emitCodemirror = (eventType?: string, event?: any) => { };
const codemirrorReady = () => { };

const setUpMarkdown = () => {
  try {
    editorJSdata.value = JSON.parse(props.cellData.cellCode);
  }
  catch (error) {
    console.log(error);
    editorJSdata.value = {};
  }

  editorJS.value = new EditorJS({
    holder: editorDom.value,
    tools: {
      header: Header
    },
    data: editorJSdata.value as any
  });
};

const setUpComment = () => {
  try {
    editorJSdata.value = JSON.parse(props.cellData.cellCode);
  }
  catch (error) {
    console.log(error);
    editorJSdata.value = {};
  }

  editorJS.value = new EditorJS({
    holder: editorDom.value,
    tools: {
      header: Header
    },
    data: editorJSdata.value as any
  });
};

onMounted(() => {
  switch (editorType.value) {
    case CellType.Comment:
      setUpComment();
      break;

    case CellType.Markdown:
      setUpMarkdown();
      break;

    case CellType.Python:
      codemirrorCode.value = props.cellData.cellCode;
      extensions.value = [python()];
      break;

    case CellType.Supercollider:
      codemirrorCode.value = props.cellData.cellCode;
      extensions.value = [python()];
      break;

    default:
      break;
  }
});

onBeforeUnmount(() => {
  if (editorJS.value)
    editorJS.value.destroy();
});
</script>
