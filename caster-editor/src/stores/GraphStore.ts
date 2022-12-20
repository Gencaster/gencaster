import { defineStore } from "pinia";
import type { Edges, Nodes } from "v-network-graph";
import type { CellType, GetGraphQuery, ScriptCell } from "@/graphql/graphql";

export const useGraphStore = defineStore({
  id: "GraphStore",
  state: () => ({
    // general data
    data: <GetGraphQuery | undefined>undefined,
    executeQuery: <any>undefined, // TODO Set correct type.

    // graph state data
    graphMapDiffers: false,

    // Server Data
    dbServerState: {},

    // current state of the user
    graphUserState: {
      nodes: <Nodes>{},
      edges: <Edges>{},
      layouts: <Nodes>{}
    },

    // TODO: Create Interface State
    // state of the data from the server
    graphServerState: {
      nodes: <Nodes>{},
      edges: <Edges>{},
      layouts: <Nodes>{}
    },

    // node editing
    defaultNewNodeName: "new scene" as string,
    defaultNewNodeColor: "standard" as string

  }),
  getters: {},
  actions: {
    updateData(data: GetGraphQuery | undefined) {
      this.data = data;
      this.dbServerState = this.data?.graph ? this.data?.graph : {};
    },
    updateQuery(query: any) {
      this.executeQuery = query;
    },
    updateGraphLocal(newNodes: any, newEdges: any, newLayout: any) {
      this.$state.graphUserState.nodes = newNodes;
      this.$state.graphUserState.edges = newEdges;
      this.$state.graphUserState.layouts = newLayout;
    },
    updateGraphServer(newNodes: any, newEdges: any, newLayout: any) {
      this.$state.graphServerState.nodes = newNodes;
      this.$state.graphServerState.edges = newEdges;
      this.$state.graphServerState.layouts = newLayout;
    },
    updateNodeScriptCellLocal(nodeUUID: string, cellCode: string, cellOrder: number, cellType: CellType, cellUUID: string) {
      const newScriptCell: ScriptCell = this.graphUserState.nodes[nodeUUID].scriptCells[cellOrder];
      newScriptCell.cellCode = cellCode;
      newScriptCell.cellOrder = cellOrder;
      newScriptCell.uuid = cellUUID;
      newScriptCell.cellType = cellType;
      this.graphUserState.nodes[nodeUUID].scriptCells[cellOrder] = newScriptCell;
    },
    updateNodeScriptCellsOrderLocal(nodeUUID: string, newScriptCellsArray: any) {
      this.$state.graphUserState.nodes[nodeUUID].scriptCells = newScriptCellsArray;
    }
  }
});
