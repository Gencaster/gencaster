import { defineStore } from "pinia";
import type { Ref } from "vue";
import type { Exact, GetNodeQuery } from "../graphql/graphql";
import { useCreateScriptCellMutation, useDeleteScriptCellMutation, useGetNodeQuery, useUpdateNodeMutation, useUpdateScriptCellsMutation } from "../graphql/graphql";

export const useNodeStore = defineStore("node", () => {
  const node: Ref<GetNodeQuery["node"]> = ref({} as GetNodeQuery["node"]);
  const fetching: Ref<boolean> = ref(true);
  const uuid: Ref<string> = ref("");

  const { executeQuery: getNodeQuery } = useGetNodeQuery({ variables: { uuid } });
  async function getNode(nodeUuid: string) {
    uuid.value = nodeUuid;
    console.log(`Get/reload node ${uuid.value} from server`);
    const { data, fetching: isFetching } = await getNodeQuery();
    if (data.value?.node)
      node.value = data.value.node;

    fetching.value = isFetching.value;
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
  const updateScriptCells = async (scriptCells: GetNodeQuery["node"]["scriptCells"]) => {
    await updateScriptCellsMutation({
      newCells: scriptCells
    }).then(() => {
      console.log(`Updated script cells ${scriptCells.map(x => x.uuid).join(",")}`);
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
    getNode,
    reloadFromServer,
    updateNode,
    createScriptCell,
    updateScriptCells,
    deleteScriptCell
  };
});
