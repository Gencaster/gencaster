import { defineStore } from "pinia";

// TODO: Setup Typescript: https://pinia.vuejs.org/core-concepts/state.html#typescript

export const useInterfaceStore = defineStore({
  id: "InterfaceStore",
  state: () => ({
    // node menu
    showNodePanel: false

  }),
  getters: {},
  actions: {}
});
