import { defineStore } from "pinia";

export const useMenuStore = defineStore({
  id: "MenuStore",
  state: () => ({
    count: 0,
    tab: "edit"
  }),
  getters: {
    doubleCount: state => state.count * 2
  },
  actions: {
    increment() {
      this.count++;
    }
  }
});
