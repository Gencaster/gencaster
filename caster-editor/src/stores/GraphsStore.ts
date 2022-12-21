import { defineStore } from "pinia";
import type { Ref } from "vue";
import type { GetGraphsQuery } from "../graphql/graphql";
import { useGetGraphsQuery } from "../graphql/graphql";

export const useGraphsStore = defineStore("graphs", () => {
  const graphs: Ref< GetGraphsQuery["graphs"] > = ref([]);
  const isFetching: Ref<boolean> = ref(true);

  async function getGraphs() {
    console.log("get graphs now");
    const { data, fetching, error } = await useGetGraphsQuery();
    if (error)
      console.log(`Could not fetch graphs: ${error.value}`);
    isFetching.value = fetching.value;
    if (data.value)
      graphs.value = data.value.graphs;
  }

  getGraphs();

  return { graphs, isFetching };
});
