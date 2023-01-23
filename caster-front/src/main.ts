import { createApp } from "vue";
import { createPinia } from "pinia";
import urql, { defaultExchanges, subscriptionExchange } from "@urql/vue";
import { SubscriptionClient } from "subscriptions-transport-ws";

import App from "./App.vue";
import router from "./router";

import "./assets/main.css";

const app = createApp(App);

app.use(urql, {
  url: import.meta.env.VITE_BACKEND_GRAPHQL_URL || "http://127.0.0.1:8081/graphql",
  requestPolicy: "network-only",
  fetchOptions: {
    credentials: "include"
  },
  exchanges: [
    ...defaultExchanges,
    subscriptionExchange({
      forwardSubscription: operation => new SubscriptionClient((import.meta.env.VITE_BACKEND_GRAPHQL_URL || "http://127.0.0.1:8081/graphql").replaceAll("https", "wss").replaceAll("http", "ws"), { reconnect: true }).request(operation)
    })
  ]
});
app.use(createPinia());
app.use(router);

app.mount("#app");
