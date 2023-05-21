<template>
  <div class="block block-codemirror">
    <div
      :class="{
        'editor-supercollider' : cellType===CellType.Supercollider,
        'editor-python' : cellType === CellType.Python}
      "
    >
      <!-- :disable="dragging" -->
      <Codemirror
        v-model="scriptText"
        placeholder="Code goes here..."
        :autofocus="false"
        :indent-with-tab="true"
        :tab-size="2"
        :extensions="[python()]"
        @ready="
          () => {
            domReady = true;
          }
        "
        @change="emitCodemirror('change')"
        @focus="emitCodemirror('focus')"
        @blur="emitCodemirror('blur')"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>

import { Codemirror } from "vue-codemirror";
import { python } from "@codemirror/lang-python";
import { computed, ref } from "vue";
import type { Ref } from "vue";
import { storeToRefs } from "pinia";
import { CellType } from "@/graphql";
import { useInterfaceStore } from "@/stores/InterfaceStore";

const props = defineProps<{
  text: string,
  cellType: CellType.Python | CellType.Supercollider
}>();
const emit = defineEmits<{
  (e: "update:text", text: string): void
}>();

const { scriptCellsModified } = storeToRefs(useInterfaceStore());

const domReady: Ref<boolean> = ref(false);

const scriptText = computed<string>({
  get() {
    return props.text
  },
  set(value) {
    emit('update:text', value);
    return value;
  },
});

const emitCodemirror = (eventType?: string) => {
  if (!domReady.value) return;

  if (eventType === "change") scriptCellsModified.value = true;
};
</script>
