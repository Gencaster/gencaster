<template>
  <div id="menu">
    <div class="menu menu-edit">
      <div class="level level-1">
        <MenuTab />
        <div class="menu-items middle">
          <span>
            {{ graph.name }}
          </span>
        </div>
        <div class="menu-items right">
          <button
            class="unstyled"
            @click="showExitGraphDialog=true"
          >
            Exit
          </button>
        </div>
      </div>
      <div class="level level-2">
        <div
          v-if="tab === Tab.Edit"
          class="left"
        >
          <MenuTabEdit
            :graph="graph"
          />
        </div>
        <div v-if="tab === Tab.Play" />
      </div>
    </div>
    <div class="menu-spacer" />

    <!-- Exit Page -->
    <DialogExitGraph
      v-if="showExitGraphDialog"
      @cancel="showExitGraphDialog=false"
    />
  </div>
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia";
import type { Graph } from "@/graphql";
import { ref, type Ref } from "vue";
import { Tab, useInterfaceStore } from "@/stores/InterfaceStore"
import MenuTab from "./MenuTabHeader.vue";
import MenuTabEdit from "./MenuTabEdit.vue";
import DialogExitGraph from "./DialogExitGraph.vue";

export type GraphMenu = Pick<Graph, 'name' | 'uuid'>;

// Props
defineProps<{
  graph: GraphMenu
}>();

// Store
const { tab } = storeToRefs(useInterfaceStore());

const showExitGraphDialog: Ref<boolean> = ref(false);

</script>
