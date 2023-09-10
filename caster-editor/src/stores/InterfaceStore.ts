import { defineStore } from "pinia";
import { type Ref, ref, computed } from "vue";
import {
  type NodeSubscription,
  type ScriptCellInputUpdate,
  type User,
  type NodeDoorInputUpdate,
  useUpdateScriptCellsMutation,
  useUpdateNodeDoorMutation,
} from "@/graphql";
import type { VueFlowStore as GraphInstance } from "@vue-flow/core";
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

  const vueFlowRef: Ref<CustomGraph | undefined> = ref(undefined);

  const tab: Ref<Tab> = ref(Tab.Edit);

  // this acts as a clutch between our local changes and the
  // updates from the server.
  const cachedNodeData: Ref<NodeSubscription | undefined> = ref(undefined);
  const newScriptCellUpdates: Ref<Map<string, ScriptCellInputUpdate>> = ref(
    new Map(),
  );
  const newNodeDoorUpdates: Ref<Map<string, NodeDoorInputUpdate>> = ref(
    new Map(),
  );
  const waitForNodeUpdate: Ref<boolean> = ref(false);

  const user: Ref<User | undefined> = ref(undefined);

  const updateScriptCellsMutation = useUpdateScriptCellsMutation();
  const updateNodeDoorMutation = useUpdateNodeDoorMutation();

  const resetUpdates = () => {
    newScriptCellUpdates.value = new Map();
    newNodeDoorUpdates.value = new Map();
  };

  const executeUpdates = async () => {
    waitForNodeUpdate.value = true;
    const scriptUpdateSuccess = await executeScriptCellUpdates();
    const nodeDoorUpdateSuccess = await executeNodeDoorUpdates();
    if (scriptUpdateSuccess && nodeDoorUpdateSuccess) {
      console.log(`Node door update is ${nodeDoorUpdateSuccess}`);
      ElMessage.success(`Successfully saved node`);
    }
    waitForNodeUpdate.value = false;
  };

  const unsavedNodeChanges = computed<boolean>((): boolean => {
    return (
      newNodeDoorUpdates.value.size > 0 || newScriptCellUpdates.value.size > 0
    );
  });

  const executeScriptCellUpdates = async (): Promise<boolean> => {
    const { error } = await updateScriptCellsMutation.executeMutation({
      scriptCellInputs: Array.from(newScriptCellUpdates.value.values()),
    });

    if (error) {
      ElMessage.error(`Could not update script cells: ${error.message}`);
      return false;
    } else {
      newScriptCellUpdates.value = new Map();
      return true;
    }
  };

  const executeNodeDoorUpdates = async (): Promise<Boolean> => {
    const toDelete: string[] = [];
    let onlySuccess = true;
    for (const [nodeDoorUUID, nodeDoor] of newNodeDoorUpdates.value) {
      const { data, error } = await updateNodeDoorMutation.executeMutation({
        ...nodeDoor,
      });
      if (data?.updateNodeDoor.__typename == "InvalidPythonCode") {
        onlySuccess = false;
        ElMessage.error({
          message: `Invalid python code on node door ${
            nodeDoor.uuid
          }<br/><pre style="white-space: pre; font-family: monospace !important;">${data.updateNodeDoor.errorMessage.replace(
            "\n",
            "<br/>",
          )}</pre>`,
          dangerouslyUseHTMLString: true,
          duration: 6000,
        });
      } else if (error) {
        onlySuccess = false;
        ElMessage.error(
          `Failed to update node door ${nodeDoorUUID}: ${error.message}`,
        );
      } else {
        toDelete.push(nodeDoorUUID);
      }
    }
    for (const uuid of toDelete) {
      newNodeDoorUpdates.value.delete(uuid);
    }
    return onlySuccess;
  };

  return {
    showNodeEditor,
    selectedNodeForEditorUuid,
    selectedNodeUUIDs,
    selectedEdgeUUIDs,
    tab,
    vueFlowRef,
    cachedNodeData,
    waitForNodeUpdate,
    newScriptCellUpdates,
    newNodeDoorUpdates,
    unsavedNodeChanges,
    resetUpdates,
    executeUpdates,
    user,
  };
});
