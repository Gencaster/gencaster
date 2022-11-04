<template>
  <div class="edit-page">
    <Graph :uuid="uuid" />
  </div>
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
