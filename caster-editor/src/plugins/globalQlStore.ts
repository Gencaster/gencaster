import { createPinia } from "pinia";
import { defineNuxtPlugin } from "#app";
import { useGraphStore } from "@/stores/GraphStore";
import { useGraphsStore } from "@/stores/GraphsStore";

export default defineNuxtPlugin((nuxtApp) => {
  const pinia = createPinia();
  nuxtApp.vueApp.use(pinia);

  nuxtApp.hook("vue:setup", () => {
    // graphs store
    const graphsStore = useGraphsStore();
    nuxtApp.graphsStore = graphsStore;

    // graph store
    const graphStore = useGraphStore();
    nuxtApp.graphStore = graphStore;
  });
});
