import { defineStore } from "pinia";
import type { Ref } from "vue";

export const useInterfaceStore = defineStore("interface", () => {
  const showEditor: Ref<boolean> = ref(false);

  return {
    showEditor
  };
});
