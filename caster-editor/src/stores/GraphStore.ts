import { defineStore } from "pinia";
import type { Edges, Nodes } from "v-network-graph";
import type { GetGraphQuery } from "@/graphql/graphql";

export const useGraphStore = defineStore({
  id: "GraphStore",
  state: () => ({
    // general data
    data: <GetGraphQuery | undefined>undefined,
    executeQuery: <any>undefined, // TODO Set correct type.

    // graph state data
    graphMapChanged: false,

    // state of the data from the server
    graphServerState: {
      nodes: <Nodes>{},
      edges: <Edges>{},
      layouts: <Nodes>{}
    },

    // current state of the user
    graphUserState: {
      nodes: <Nodes>{},
      edges: <Edges>{},
      layouts: <Nodes>{}
    },

    // node editing
    defaultNewNodeName: "new scene" as string,
    defaultNewNodeColor: "standard" as string,

    // node menu
    showNodePanel: false

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
