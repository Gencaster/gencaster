import { defineStore } from "pinia";

export const useGraphStore = defineStore({
  id: "GraphStore",
  state: () => ({
    count: 0

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
