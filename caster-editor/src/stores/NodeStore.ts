import { defineStore } from "pinia";
import type { Ref } from "vue";
import type { Exact, GetNodeQuery, ScriptCellInput } from "../graphql/graphql";
import { useCreateScriptCellMutation, useDeleteScriptCellMutation, useGetNodeQuery, useUpdateNodeMutation, useUpdateScriptCellsMutation } from "../graphql/graphql";

export const useNodeStore = defineStore("node", () => {
  const node: Ref<GetNodeQuery["node"]> = ref({} as GetNodeQuery["node"]);
  const fetching: Ref<boolean> = ref(true);
  const uuid: Ref<string> = ref("");
  const scriptCellsModified: Ref<boolean> = ref(false);

  const { executeQuery: getNodeQuery } = useGetNodeQuery({ variables: { nodeUuid: uuid }, pause: true });
  async function getNode(nodeUuid: string) {
    uuid.value = nodeUuid;
    console.log(`Get/reload node ${uuid.value} from server`);
    const { data, fetching: isFetching, error } = await getNodeQuery();
    if (data.value?.node) {
      node.value = data.value.node;
      fetching.value = isFetching.value;
    }
    if (error.value)
      console.log(`Error fetching node data of ${nodeUuid}`, error.value);
  }

  const reloadFromServer = async () => {
    await getNode(node.value.uuid);
  };

  const { executeMutation: updateNodeMutation } = useUpdateNodeMutation();
  const updateNode = async (node: GetNodeQuery["node"]) => {
    await updateNodeMutation({
      nodeUuid: node.uuid,
      ...node
    });
    await reloadFromServer();
  };

  const { executeMutation: createScriptCellMutation } = useCreateScriptCellMutation();
  const createScriptCell = async (scriptCell: Exact<{ nodeUuid: any; order: number }>) => {
    await createScriptCellMutation(scriptCell);
    await reloadFromServer();
  };

  const { executeMutation: updateScriptCellsMutation } = useUpdateScriptCellsMutation();
  const updateScriptCells = async (scriptCells: Array<ScriptCellInput>) => {
    for (const cell of scriptCells) {
      // @ts-expect-error: somehow the object has __typename which the API does not like
      delete cell.__typename;
    }

    await updateScriptCellsMutation({
      newCells: scriptCells
    }).then(() => {
      console.log(`Updated script cells ${scriptCells.map(x => x.uuid).join(",")}`);
      scriptCellsModified.value = false;
    });
    await reloadFromServer();
  };

  const { executeMutation: deleteScriptCellMutation } = useDeleteScriptCellMutation();
  const deleteScriptCell = async (scriptCellUuid: any) => {
    await deleteScriptCellMutation({ scriptCellUuid }).then(() =>
      console.log(`Deleted script cell ${scriptCellUuid}`)
    );
    await reloadFromServer();
  };

  return {
    node,
    fetching,
    scriptCellsModified,
    getNode,
    reloadFromServer,
    updateNode,
    createScriptCell,
    updateScriptCells,
    deleteScriptCell
  };
});
