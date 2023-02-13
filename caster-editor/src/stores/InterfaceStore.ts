import { defineStore } from "pinia";
import { type Ref, ref } from "vue";

export const useInterfaceStore = defineStore("interface", () => {
  const showEditor: Ref<boolean> = ref(false);

  return {
    showEditor,
  };
});
