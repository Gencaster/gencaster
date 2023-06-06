import { defineStore } from "pinia";
import { type Ref, ref } from "vue";
import type { Node, User } from "@/graphql";
import type { Instance as GraphInstance } from "v-network-graph";

export enum Tab {
  Edit = "Edit",
  Play = "Play",
}

// some hack to avoid
// https://github.com/microsoft/TypeScript/issues/5711
interface CustomGraph extends GraphInstance {
}

export const useInterfaceStore = defineStore("interface", () => {
  const showNodeEditor: Ref<boolean> = ref(false);

  const selectedNode: Ref<Node | undefined> = ref(undefined);
  const selectedNodeUUIDs: Ref<string[]> = ref([]);
  const selectedEdgeUUIDs: Ref<string[]> = ref([]);

  const vNetworkGraph: Ref<CustomGraph | undefined> = ref(undefined);

  const tab: Ref<Tab> = ref(Tab.Edit);

  const scriptCellsModified: Ref<boolean> = ref(false);

  const user: Ref<User | undefined> = ref(undefined);

  return {
    showNodeEditor,
    selectedNode,
    selectedNodeUUIDs,
    selectedEdgeUUIDs,
    tab,
    vNetworkGraph,
    scriptCellsModified,
    user,
  };
});
