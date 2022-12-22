import { defineStore } from "pinia";
import type { Ref } from "vue";

export const useInterfaceStore = defineStore("interface", () => {
  const showNodePanel: Ref<boolean> = ref(false);

  return {
    showNodePanel
  };
});
