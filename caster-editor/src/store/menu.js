import { defineStore } from "pinia";

export const useMenuStore = defineStore({
  id: "menu-store",
  state: () => {
    return {
      filtersList: ["youtube", "twitch"]
    };
  },
  actions: {},
  getters: {
    filtersList: state => state.filtersList
  }
});
