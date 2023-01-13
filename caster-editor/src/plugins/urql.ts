import urql, { defaultExchanges, subscriptionExchange } from "@urql/vue";
import { SubscriptionClient } from "subscriptions-transport-ws";

import { defineNuxtPlugin } from "#app";
import { useRuntimeConfig } from "#imports";

const subscriptionClient = new SubscriptionClient("ws://127.0.0.1:8081/graphql", { reconnect: true });

export default defineNuxtPlugin((nuxtApp: any) => {
  const config = useRuntimeConfig();

  nuxtApp.vueApp.use(urql, {
    url: config.public.BACKEND_GRAPHQL_URL,
    exchanges: [
      ...defaultExchanges,
      subscriptionExchange({
        forwardSubscription: operation => subscriptionClient.request(operation)
      })
    ],
    requestPolicy: "network-only",
    fetchOptions: {
      credentials: "include"
    }
  });
});
