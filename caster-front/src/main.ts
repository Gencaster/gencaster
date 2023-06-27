import { createApp } from "vue";
import { createPinia } from "pinia";
import urql, { fetchExchange, subscriptionExchange } from "@urql/vue";
import { SubscriptionClient } from "subscriptions-transport-ws";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";

import App from "./App.vue";
import router from "./router";

import "./assets/main.scss";

const app = createApp(App);

app.use(urql, {
  url: `${import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8081"}/graphql`,
  requestPolicy: "network-only",
  fetchOptions: {
    credentials: "include",
  },
  exchanges: [
    fetchExchange,
    subscriptionExchange({
      forwardSubscription: (operation) =>
        new SubscriptionClient(
          `${
            import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8081"
          }/graphql`
            .replace("https", "wss")
            .replace("http", "ws"),
          { reconnect: true },
        ).request(operation),
    }),
  ],
});
app.use(createPinia());
app.use(router);
app.use(ElementPlus);

app.mount("#app");
