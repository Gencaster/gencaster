<script lang="ts">
export default {
  name: "UuidWrapper",

  data() {
    return {};
  },
  computed: {
    uuid() {
      return this.$route.params.uuid;
    }
  },
  mounted() {},
  methods: {}
};
</script>

<template>
  <div class="edit-page">
    <Graph :uuid="uuid" />
  </div>
</template>
