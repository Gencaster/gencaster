import { createApp } from "vue";
import { createPinia } from "pinia";
import urql from "@urql/vue";

import App from "./App.vue";
import router from "./router";

import "./assets/main.css";

const app = createApp(App);

app.use(urql, {
  url: "http://127.0.0.1:8081/graphql",
  requestPolicy: "network-only",
  fetchOptions: {
    credentials: "include"
  }
});
app.use(createPinia());
app.use(router);

app.mount("#app");
