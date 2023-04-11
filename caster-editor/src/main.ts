import { createApp } from "vue";
import { createPinia } from "pinia";
import urql, { subscriptionExchange, dedupExchange, cacheExchange } from "@urql/vue";
import VNetworkGraph from "v-network-graph";
import { SubscriptionClient } from "subscriptions-transport-ws";
import { multipartFetchExchange } from '@urql/exchange-multipart-fetch';
import "v-network-graph/lib/style.css";

import ElementPlus from "element-plus";
import "element-plus/dist/index.css";

import App from "@/App.vue";
import router from "@/router";

import "./assets/scss/main.scss";
import "v-network-graph/lib/style.css";

const app = createApp(App);
app.use(router);

app.use(urql, {
  url:
    `${import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8081"}/graphql`,
  requestPolicy: "network-only",
  fetchOptions: {
    credentials: "include",
  },
  exchanges: [
    dedupExchange,
    cacheExchange,
    multipartFetchExchange,
    subscriptionExchange({
      forwardSubscription: (operation) =>
        new SubscriptionClient(
            `${import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8081"}/graphql`
            .replace("https", "wss")
            .replace("http", "ws"),
          { reconnect: true }
        ).request(operation),
    }),
  ],
});
app.use(createPinia());
app.use(VNetworkGraph);
app.use(ElementPlus);
app.mount("#app");
