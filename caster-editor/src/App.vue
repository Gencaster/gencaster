<script setup lang="ts">
import { RouterView } from "vue-router";
import LoginDialog from "@/components/LoginDialog.vue";

import { useIsAuthenticatedQuery } from "@/graphql";
import { watch, type Ref, ref } from "vue";
import { useInterfaceStore } from "@/stores/InterfaceStore";
import { storeToRefs } from "pinia";
import { ElMessage } from "element-plus";

const {user} = storeToRefs(useInterfaceStore());

const { data, error } = useIsAuthenticatedQuery();

// when fetching=false it resolves authenticated - this takes a
// split of a second which displays the login form, therefore
// we resolve it manually here
const resolvedLoginState: Ref<boolean> = ref(false);

watch(data, (d) => {
  if(d?.isAuthenticated) {
     user.value = d.isAuthenticated;
  }
  resolvedLoginState.value = true;
});

watch(error, (e) => {
  if(e?.message) {
    ElMessage.error(`Please log in: ${e.message}`);
  }
  resolvedLoginState.value = true;
});

</script>

<template>
  <div
    v-loading="!resolvedLoginState"
    class="main"
  >
    <div
      v-if="user === undefined"
      class="login"
    >
      <LoginDialog />
    </div>
    <div v-else>
      <RouterView />
    </div>
  </div>
</template>
