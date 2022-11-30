<template>
  <div class="node-editor-outer">
    I'm the node editor
    {{ dev }}
    {{ blockData }}
  </div>
</template>

<script lang="ts">
export default {
  name: "NodeEditor",

  props: {
    dev: {
      type: Boolean,
      required: false,
      default: () => false
    },
    blockData: {
      type: Array,
      required: true,
      default: () => []
    }
  },

  data() {
    return {};
  },

  computed: {
  },

  mounted() {
  }
};
</script>

<style lang="scss">
.node-editor-outer {
  height: inherit;
  widows: inherit;
  padding: 10px;
  background-color: $mainWhite;
  border: 1px solid $black;
}
</style>
