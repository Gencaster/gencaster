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
            @click="goToDocs()"
          >
            Docs
          </button>
          <button
            class="unstyled"
            @click="showExitGraphDialog = true"
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
          <MenuTabEdit :graph="graph" />
        </div>
        <div v-if="tab === Tab.Play" />
      </div>
    </div>
    <div class="menu-spacer" />

    <!-- Exit Page -->
    <DialogExitGraph
      v-if="showExitGraphDialog"
      @cancel="showExitGraphDialog = false"
    />
  </div>
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia";
import type { Graph } from "@/graphql";
import { ref, type Ref } from "vue";
import { Tab, useInterfaceStore } from "@/stores/InterfaceStore";
import MenuTab from "./MenuTabHeader.vue";
import MenuTabEdit from "./MenuTabEdit.vue";
import DialogExitGraph from "./DialogExitGraph.vue";

export type GraphMenu = Pick<Graph, "name" | "uuid">;

// Props
defineProps<{
  graph: GraphMenu;
}>();

// Store
const { tab } = storeToRefs(useInterfaceStore());

const showExitGraphDialog: Ref<boolean> = ref(false);

const goToDocs = () => {
  window.open("https://docs.gencaster.org/", "_blank");
};
</script>

<style lang="scss" scoped>
@import "@/assets/scss/variables.module.scss";

.menu {
  width: 100vw;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;

  .level {
    height: $menuHeight;
    background-color: $grey-light;
    border-bottom: 1px solid $black;
    padding-left: $paddingSidesDesktop;
    padding-right: $paddingSidesDesktop;

    display: flex;
    justify-content: space-between;
    align-items: center;

    .left {
      transform: translateX(-8px);
      width: 33%;
    }

    &.level-2 {

      .left,
      .middle,
      .right {
        width: auto;
      }
    }

    .middle {
      width: 33%;
      display: flex;
      justify-content: center;
    }

    .right {
      transform: translateX(8px);
      width: 33%;
      display: flex;
      justify-content: flex-end;
    }

    .menu-items {
      height: 30px;
      display: flex;
      align-items: center;

      .state {
        display: flex;
        justify-content: center;
        align-items: center;
      }

      .state-indicator {
        width: 11px;
        height: 11px;
        border-radius: 11px;
        background-color: $alertRed;
        margin-right: 4px;

        &.saved {
          background-color: $green-light;
        }
      }
    }

    .margin-left {
      margin-left: $buttonMargin;
    }

    .margin-right {
      margin-right: $buttonMargin;
    }
  }
}

.menu-spacer {
  position: relative;
  height: 64px;
  background-color: white;
}
</style>
