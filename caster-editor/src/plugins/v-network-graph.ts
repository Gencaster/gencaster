import VNetworkGraph from "v-network-graph";
import { defineNuxtPlugin } from "#app";

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(VNetworkGraph);
});
