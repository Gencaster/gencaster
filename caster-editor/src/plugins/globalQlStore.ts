import { createPinia } from "pinia";
import { defineNuxtPlugin } from "#app";
import { useMenuStore } from "@/stores/MenuStore";
import { useGraphStore } from "@/stores/GraphStore";
import { useGraphsStore } from "@/stores/GraphsStore";
import { useInterfaceStore } from "@/stores/InterfaceStore";
import { useNodeStore } from "@/stores/NodeStore";

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

    // menu store
    const menuStore = useMenuStore();
    nuxtApp.menuStore = menuStore;

    // interface store
    const interfaceStore = useInterfaceStore();
    nuxtApp.interfaceStore = interfaceStore;

    // node store
    const nodeStore = useNodeStore();
    nuxtApp.nodeStore = nodeStore;
  });
});
