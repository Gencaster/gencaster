<template>
  <div>
    <div class="editor-wrapper">
      <div class="editor-inner">
        <ElementsBlockEditor :dev="true" :blocks-data="debugBlockData" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { debugBlockData } from "@/assets/js/dev/debugBlockData";

export default {
  name: "BlockEditorTestPage",

  data() {
    return {
      debugBlockData: []
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
</style>
