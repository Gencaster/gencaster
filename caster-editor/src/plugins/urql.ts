import urql from "@urql/vue";
// @ts-expect-error: Auto Imported by nuxt
import { defineNuxtPlugin } from "#app";

export default defineNuxtPlugin((nuxtApp) => {
  // @ts-expect-error: Auto Imported by nuxt
  const config = useRuntimeConfig();

  nuxtApp.vueApp.use(urql, {
    url: config.public.BACKEND_GRAPHQL_URL,
    requestPolicy: "network-only",
    fetchOptions: {
      credentials: "include"
    }
  });
});
