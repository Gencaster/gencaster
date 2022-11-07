import { defineNuxtPlugin } from "#app";
import urql from '@urql/vue';

export default defineNuxtPlugin((nuxtApp) => {
    const config = useRuntimeConfig();

    nuxtApp.vueApp.use(urql, {
        url: config.public.BACKEND_GRAPHQL_URL,
        requestPolicy: 'network-only',
        fetchOptions: {
            credentials: 'include'
          }
    });
});
