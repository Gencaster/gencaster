import { defineStore } from "pinia";
import type { Ref } from "vue";
import type { Exact, GraphSubscription, NewScriptCellInput, Scalars, ScriptCellInput } from "@/graphql/graphql";
import { useCreateScriptCellMutation, useDeleteScriptCellMutation, useNodeSubscription, useUpdateNodeMutation, useUpdateScriptCellsMutation } from "@/graphql/graphql";

export const useNodeStore = defineStore("node", () => {
  const uuid: Ref<string> = ref("");
  const scriptCellsModified: Ref<boolean> = ref(false);

  const { data: node, error, fetching } = useNodeSubscription({ variables: { uuid }, pause: false });

  const { executeMutation: updateNodeMutation } = useUpdateNodeMutation();
  const updateNode = async (node: GraphSubscription["graph"]["nodes"][0]) => {
    await updateNodeMutation({
      nodeUuid: node.uuid,
      ...node
    });
  };

  const { executeMutation: createScriptCellMutation } = useCreateScriptCellMutation();
  const createScriptCell = async (scriptCell: Exact<{ nodeUuid: Scalars["UUID"]; newScriptCell: NewScriptCellInput }>) => {
    await createScriptCellMutation(scriptCell);
  };

  const { executeMutation: updateScriptCellsMutation } = useUpdateScriptCellsMutation();
  const updateScriptCells = async (scriptCells: Array<ScriptCellInput>) => {
    for (const cell of scriptCells) {
      // @ts-expect-error: somehow the object has __typename which the API does not like
      // TODO: this is because of the GraphQL settings. It passes a hard coded scriptcell with __typename
      delete cell.__typename;
    }

    await updateScriptCellsMutation({
      newCells: scriptCells
    }).then(() => {
      console.log(`Updated script cells ${scriptCells.map(x => x.uuid).join(",")}`);
      scriptCellsModified.value = false;
    });
  };

  const { executeMutation: deleteScriptCellMutation } = useDeleteScriptCellMutation();
  const deleteScriptCell = async (scriptCellUuid: any) => {
    await deleteScriptCellMutation({ scriptCellUuid }).then(() =>
      console.log(`Deleted script cell ${scriptCellUuid}`)
    );
  };

  return {
    node,
    fetching,
    error,
    uuid,
    scriptCellsModified,
    updateNode,
    createScriptCell,
    updateScriptCells,
    deleteScriptCell
  };
});
