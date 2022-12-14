import { defineStore } from "pinia";

// TODO: Setup Typescript: https://pinia.vuejs.org/core-concepts/state.html#typescript

export const useMenuStore = defineStore({
  id: "MenuStore",
  state: () => ({
    count: 0,
    tab: "edit",

    // savestates
    nodesChanged: false, // if nodes have been moved around
    blocksChanged: false // if blocks of a node has changed

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
