import urql, { defaultExchanges, subscriptionExchange } from "@urql/vue";
import { SubscriptionClient } from "subscriptions-transport-ws";

import { defineNuxtPlugin } from "#app";
import { useRuntimeConfig } from "#imports";

export default defineNuxtPlugin((nuxtApp: any) => {
  const config = useRuntimeConfig();

  nuxtApp.vueApp.use(urql, {
    url: config.public.BACKEND_GRAPHQL_URL,
    exchanges: [
      ...defaultExchanges,
      subscriptionExchange({
        forwardSubscription: operation => new SubscriptionClient(config.public.BACKEND_GRAPHQL_URL.replaceAll("https", "wss").replaceAll("http", "ws"), { reconnect: true }).request(operation)
      })
    ],
    requestPolicy: "network-only",
    fetchOptions: {
      credentials: "include"
    }
  });
});
