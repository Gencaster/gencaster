import { createApp } from "vue";
import { createPinia } from "pinia";
import urql, {
  subscriptionExchange,
  dedupExchange,
  cacheExchange,
} from "@urql/vue";
import VNetworkGraph from "v-network-graph";
import { SubscriptionClient } from "subscriptions-transport-ws";
import { multipartFetchExchange } from "@urql/exchange-multipart-fetch";
import "v-network-graph/lib/style.css";
import * as Sentry from "@sentry/vue";

import ElementPlus from "element-plus";
import "element-plus/dist/index.css";

import App from "@/App.vue";
import router from "@/router";

import "./assets/scss/main.scss";
import "v-network-graph/lib/style.css";

import "@vue-flow/core/dist/style.css";
/* this contains the default theme, these are optional styles */
import "@vue-flow/core/dist/theme-default.css";

const app = createApp(App);

if (
  import.meta.env.VITE_BACKEND_URL &&
  import.meta.env.VITE_SENTRY_DSN_CASTER_EDITOR
) {
  Sentry.init({
    app,
    dsn: import.meta.env.VITE_SENTRY_DSN_CASTER_EDITOR,
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

app.use(router);

app.use(urql, {
  url: `${import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8081"}/graphql`,
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
app.use(VNetworkGraph);
app.use(ElementPlus);
app.mount("#app");
