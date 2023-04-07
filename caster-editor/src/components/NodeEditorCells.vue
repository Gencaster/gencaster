<!-- eslint-disable vue/no-unused-vars -->
<template>
  <div class="blocks">
    <draggable
      v-model="moveableScriptCells"
      group="blocks"
      item-key="uuid"
      @start="drag=true"
      @end="drag=false"
    >
      <!-- hack is necessary to track v-for with v-model, see
        https://stackoverflow.com/a/71378972
      -->
      <template #item="{element, index}">
        <div>
          <NodeEditorCell
            v-if="moveableScriptCells[index]"
            v-model:script-cell="moveableScriptCells[index]"
          />
        </div>
      </template>
    </draggable>
  </div>
</template>

<script setup lang="ts">
import type { NodeSubscription } from "@/graphql";
import { useInterfaceStore } from "@/stores/InterfaceStore";
import { storeToRefs } from "pinia";
import { computed, ref, type Ref } from "vue";
import draggable from 'vuedraggable';
import NodeEditorCell from "./NodeEditorCell.vue";

const props = defineProps<{
    scriptCells: NodeSubscription['node']['scriptCells'],
}>();

const drag: Ref<boolean> = ref(false);
const {scriptCellsModified} = storeToRefs(useInterfaceStore());

const emit = defineEmits(['update:scriptCells'])

const moveableScriptCells = computed<NodeSubscription['node']['scriptCells']>({
    get() {
        return props.scriptCells;
    },
    set(value) {
        scriptCellsModified.value = true;
        emit('update:scriptCells', value)
        return value;
    }
});

</script>
