import { defineStore } from "pinia";
import type { GetGraphQuery } from "../graphql/graphql";

export const useGraphStore = defineStore({
  id: "GraphStore",
  state: () => ({
    // data
    data: <GetGraphQuery | undefined>undefined,
    executeQuery: <any>undefined, // TODO Set correct type.

    // node editing
    defaultNewNodeName: "new scene" as string,
    defaultNewNodeColor: "standard" as string

  }),
  getters: {},
  actions: {
    updateData(data: GetGraphQuery | undefined) {
      this.data = data;
    },
    updateQuery(query: any) {
      this.executeQuery = query;
    }
  }
});
