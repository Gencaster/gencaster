<script lang="ts" setup>
import { computed, ref } from "vue";
import type { Ref } from "vue";
import { storeToRefs } from "pinia";
import { CellType } from "@/graphql";
import { useInterfaceStore } from "@/stores/InterfaceStore";

// Codemirror
import { Codemirror } from "vue-codemirror";
import { python, pythonLanguage } from "@codemirror/lang-python";

// autocomplete
import completePython from "@/assets/js/completePython";
import completeSC from "@/assets/js/completeSC";

const props = defineProps<{
  text: string;
  cellType: CellType.Python | CellType.Supercollider;
  uuid: string;
}>();

const { newScriptCellUpdates } = storeToRefs(useInterfaceStore());

const domReady: Ref<boolean> = ref(false);

const scriptText = computed<string>({
  get() {
    return props.text;
  },
  set(value) {
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

// autocomplete
const pythonDocCompletions = pythonLanguage.data.of({
  autocomplete: completePython,
});

// TODO: add scDocCompletions. Not working like this
const scDocCompletions = pythonLanguage.data.of({
  autocomplete: completeSC,
});

// extensions
const extensions = computed(() => {
  if (props.cellType === CellType.Python) {
    return [python(), pythonDocCompletions];
  } else {
    return [];
  }
});
</script>

<template>
  <div class="block block-codemirror">
    <div
      :class="{
        'editor-supercollider': cellType === CellType.Supercollider,
        'editor-python': cellType === CellType.Python,
      }"
    >
      <!-- :disable="dragging" -->
      <Codemirror
        v-model="scriptText"
        placeholder="Code goes here..."
        :autofocus="false"
        :indent-with-tab="true"
        :tab-size="2"
        :extensions="extensions"
        @ready="
          () => {
            domReady = true;
          }
        "
      />
    </div>
  </div>
</template>
