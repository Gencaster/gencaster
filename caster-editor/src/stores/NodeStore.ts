import { defineStore } from "pinia";
import { type Ref, computed, ref } from "vue";
import type {
  Exact,
  GraphSubscription,
  NewScriptCellInput,
  Scalars,
  ScriptCellInput,
} from "@/graphql";
import {
  useCreateScriptCellMutation,
  useDeleteScriptCellMutation,
  useNodeSubscription,
  useUpdateNodeMutation,
  useUpdateScriptCellsMutation,
} from "@/graphql";

export const useNodeStore = defineStore("node", () => {
  const uuid: Ref<string | undefined> = ref(undefined);
  const scriptCellsModified: Ref<boolean> = ref(false);

  const pauseSubscription = computed(() => {return uuid.value === undefined});

  const {
    data: node,
    error,
    fetching,
    stale,
  } = useNodeSubscription({ variables: { uuid }, pause: pauseSubscription });

  const nodeDataReady = computed(() => {return uuid.value === node.value?.node.uuid});


  const { executeMutation: updateNodeMutation } = useUpdateNodeMutation();
  const updateNode = async (node: GraphSubscription["graph"]["nodes"][0]) => {
    await updateNodeMutation({
      nodeUuid: node.uuid,
      ...node,
    });
  };

  const { executeMutation: createScriptCellMutation } =
    useCreateScriptCellMutation();
  const createScriptCell = async (
    scriptCell: Exact<{
      nodeUuid: Scalars["UUID"];
      newScriptCell: NewScriptCellInput;
    }>
  ) => {
    await createScriptCellMutation(scriptCell);
  };

  const { executeMutation: updateScriptCellsMutation } =
    useUpdateScriptCellsMutation();
  const updateScriptCells = async (scriptCells: Array<ScriptCellInput>) => {
    await updateScriptCellsMutation({
      newCells: scriptCells,
    }).then(() => {
      console.log(
        `Updated script cells ${scriptCells.map((x) => x.uuid).join(",")}`
      );
      scriptCellsModified.value = false;
    });
  };

  const { executeMutation: deleteScriptCellMutation } =
    useDeleteScriptCellMutation();
  const deleteScriptCell = async (scriptCellUuid: any) => {
    await deleteScriptCellMutation({ scriptCellUuid }).then(() =>
      console.log(`Deleted script cell ${scriptCellUuid}`)
    );
  };

  return {
    node,
    fetching,
    error,
    stale,
    uuid,
    scriptCellsModified,
    updateNode,
    createScriptCell,
    updateScriptCells,
    deleteScriptCell,
    nodeDataReady,
  };
});
