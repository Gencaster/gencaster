import { defineStore } from "pinia";
import { type Ref, ref } from "vue";
import {
  type NodeSubscription,
  type ScriptCellInputUpdate,
  type User,
  useUpdateScriptCellsMutation,
} from "@/graphql";
import type { Instance as GraphInstance } from "v-network-graph";
import { ElMessage } from "element-plus";

export enum Tab {
  Edit = "Edit",
  Play = "Play",
}

// some hack to avoid
// https://github.com/microsoft/TypeScript/issues/5711
interface CustomGraph extends GraphInstance {}

export const useInterfaceStore = defineStore("interface", () => {
  const showNodeEditor: Ref<boolean> = ref(false);

  const selectedNodeForEditorUuid: Ref<string | undefined> = ref(undefined);
  const selectedNodeUUIDs: Ref<string[]> = ref([]);
  const selectedEdgeUUIDs: Ref<string[]> = ref([]);

  const vNetworkGraph: Ref<CustomGraph | undefined> = ref(undefined);

  const tab: Ref<Tab> = ref(Tab.Edit);

  // this acts as a clutch between our local changes and the
  // updates from the server.
  const cachedNodeData: Ref<NodeSubscription | undefined> = ref(undefined);
  const newScriptCellUpdates: Ref<Map<string, ScriptCellInputUpdate>> = ref(
    new Map(),
  );
  const waitForScriptCellsUpdate: Ref<boolean> = ref(false);

  const user: Ref<User | undefined> = ref(undefined);

  const updateScriptCellsMutation = useUpdateScriptCellsMutation();

  const resetScriptCellUpdates = () => {
    newScriptCellUpdates.value = new Map();
  };

  const executeScriptCellUpdates = async () => {
    waitForScriptCellsUpdate.value = true;

    const { error } = await updateScriptCellsMutation.executeMutation({
      scriptCellInputs: Array.from(newScriptCellUpdates.value.values()),
    });

    if (error) {
      ElMessage.error(`Could not update script cells: ${error.message}`);
      waitForScriptCellsUpdate.value = false;
      return;
    } else {
      resetScriptCellUpdates();
      ElMessage.success(`Successfully saved script cells`);
    }
  };

  return {
    showNodeEditor,
    selectedNodeForEditorUuid,
    selectedNodeUUIDs,
    selectedEdgeUUIDs,
    tab,
    vNetworkGraph,
    cachedNodeData,
    waitForScriptCellsUpdate,
    newScriptCellUpdates,
    resetScriptCellUpdates,
    executeScriptCellUpdates,
    user,
  };
});
