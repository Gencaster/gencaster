<template>
  <div class="edit-page">
    <div class="editor-wrapper">
      <div class="editor-inner">
        <div class="node-data">
          <ElementsBlockEditor :dev="true" :blocks-data="debugBlockData" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { debugBlockData } from "@/assets/js/dev/debugBlockData";
import type { ScriptCell } from "@/graphql/graphql";

export default {
  name: "BlockEditorTestPage",

  data() {
    return {
      debugBlockData: [] as ScriptCell[]
    };
  },

  computed: {
  },

  mounted() {
    this.debugBlockData = debugBlockData;
  }
};
</script>

<style lang="scss">
.edit-page {
  .editor-wrapper {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    background-color: white;
    width: 100vw;
    height: 100vh;
    padding: 20px;

    .editor-inner {
      width: 50%;
      height: 100%;
    }
  }
}
</style>
