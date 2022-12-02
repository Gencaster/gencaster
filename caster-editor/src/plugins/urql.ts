import urql from "@urql/vue";

import { defineNuxtPlugin } from "#app";
import { useRuntimeConfig } from "#imports";

export default defineNuxtPlugin((nuxtApp: any) => {
  const config = useRuntimeConfig();

  nuxtApp.vueApp.use(urql, {
    url: config.public.BACKEND_GRAPHQL_URL,
    requestPolicy: "network-only",
    fetchOptions: {
      credentials: "include"
    }
  });
});
