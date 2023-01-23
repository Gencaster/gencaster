import { defineStore } from "pinia";
import type { Ref } from "vue";

export enum Tab {
  Edit = "Edit",
  Play = "Play"
}

export const useMenuStore = defineStore("menu", () => {
  const tab: Ref<Tab> = ref(Tab.Edit);

  return { tab };
});
