import { defineStore } from "pinia";
import type { Ref } from "vue";
import type { GetGraphsQuery } from "@/graphql/graphql";
import { useGetGraphsQuery } from "@/graphql/graphql";

export const useGraphsStore = defineStore("graphs", () => {
  const graphs: Ref< GetGraphsQuery["graphs"] > = ref([]);
  const fetching: Ref<boolean> = ref(true);

  async function getGraphs() {
    const { data, fetching: isFetching, error } = await useGetGraphsQuery();
    if (error.value)
      console.log("Could not fetch graphs", error);
    fetching.value = isFetching.value;
    if (data.value)
      graphs.value = data.value.graphs;
  }

  getGraphs();

  return { graphs, fetching };
});
