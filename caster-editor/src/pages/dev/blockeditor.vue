<template>
  <div>
    <div class="editor-wrapper">
      <div class="editor-inner">
        <ElementsNodeEditor />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: "BlockEditorTestPage",

  data() {
    return {};
  },

  computed: {
  },

  mounted() {
    console.log("yeah");
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
