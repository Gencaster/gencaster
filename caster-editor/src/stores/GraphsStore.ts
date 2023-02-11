import { defineStore } from "pinia";
import { type Ref, ref } from "vue";
import type { AddGraphInput, GetGraphsQuery } from "@/graphql";
import { useGetGraphsQuery, useCreateGraphMutation } from "@/graphql";
import type { CombinedError } from "@urql/vue";

export const useGraphsStore = defineStore("graphs", () => {
  const graphs: Ref<GetGraphsQuery["graphs"]> = ref([]);
  const fetching: Ref<boolean> = ref(true);

  const graphsQuery = useGetGraphsQuery();
  async function getGraphs() {
    const { data, fetching: isFetching, error } = await graphsQuery.executeQuery();
    if (error.value) {
      console.log("Could not fetch graphs", error);
    }
    fetching.value = isFetching.value;
    if (data.value) {
      graphs.value = data.value.graphs;
    }
  }

  const createGraphMutation = useCreateGraphMutation();
  async function createGraph(graphInput: AddGraphInput): Promise<CombinedError | undefined> {
    const { error } = await createGraphMutation.executeMutation({graphInput});
    if (error) {
      console.log("Error on creating graph" + error);
    }
    await getGraphs();
    return error;
  }

  getGraphs();

  return { graphs, fetching, createGraph };
});
