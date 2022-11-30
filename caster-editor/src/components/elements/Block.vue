<template>
  <div>
    {{ cellData }}
  </div>
</template>

<script>
export default {
  components: {},

  props: {
    cellData: {
      type: Object,
      required: true,
      default: () => {}
    }
  },

  data() {
    return {
    };
  },

  watch: {},

  mounted() {},

  beforeUnmount() {}
};
</script>
