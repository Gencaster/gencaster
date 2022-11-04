<template>
  <Graph :uuid="uuid" />
</template>

<script lang="ts">
export default {
  name: 'uuidWrapper',

  data() {
    return {};
  },
  computed: {
    uuid() {
      return this.$route.params.uuid;
    },
  },
  mounted() {},
  methods: {},
};
</script>
