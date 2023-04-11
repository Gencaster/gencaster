<script setup lang="ts">
import { RouterView } from "vue-router";
import { ElMessageBox } from "element-plus";

import { useIsAuthenticatedQuery } from "@/graphql"
import { watch } from "vue";

const { error, fetching } = useIsAuthenticatedQuery();

watch(error, (e) => {
  if(e?.message) {
    ElMessageBox.alert(`Please login: ${e.message}`, {
      closeOnClickModal: false,
      closeOnPressEscape: false,
      showClose: false,
      showConfirmButton: false
    });
  }
});

</script>

<template>
  <RouterView
    v-if="!error"
    v-loading="fetching"
  />
</template>
