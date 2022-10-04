import { defineNuxtPlugin } from "#app";
import urql from '@urql/vue';

export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.vueApp.use(urql, {
        url: 'http://localhost:8081/graphql',
        requestPolicy: 'network-only',
    });
});
