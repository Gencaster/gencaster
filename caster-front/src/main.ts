import { createApp } from "vue";
import { createHead } from "@unhead/vue";
import { createPinia } from "pinia";
import urql, { fetchExchange, subscriptionExchange } from "@urql/vue";
import { SubscriptionClient } from "subscriptions-transport-ws";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import * as Sentry from "@sentry/vue";

import App from "./App.vue";
import router from "./router";

import "./assets/main.scss";

const app = createApp(App);

const head = createHead();
app.use(head);

if (
  import.meta.env.VITE_BACKEND_URL &&
  import.meta.env.VITE_SENTRY_DSN_CASTER_FRONT
) {
  Sentry.init({
    app,
    dsn: import.meta.env.VITE_SENTRY_DSN_CASTER_FRONT,
    integrations: [
      new Sentry.BrowserTracing({
        routingInstrumentation: Sentry.vueRouterInstrumentation(router),
      }),
      new Sentry.Replay(),
    ],
    // Performance Monitoring
    tracesSampleRate: 1.0, // Capture 100% of the transactions, reduce in production!
    // Session Replay
    replaysSessionSampleRate: 0.5, // This sets the sample rate at 10%. You may want to change it to 100% while in development and then sample at a lower rate in production.
    replaysOnErrorSampleRate: 1.0, // If you're not already sampling the entire session, change the sample rate to 100% when sampling sessions where errors occur.
  });
}

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
