import { defineStore } from "pinia";
import { type Ref, ref } from "vue";
import type { GetGraphsQuery } from "@/graphql";
import { useGetGraphsQuery } from "@/graphql";

export const useGraphsStore = defineStore("graphs", () => {
  const graphs: Ref<GetGraphsQuery["graphs"]> = ref([]);
  const fetching: Ref<boolean> = ref(true);

  async function getGraphs() {
    const { data, fetching: isFetching, error } = await useGetGraphsQuery();
    console.log(useGetGraphsQuery)
    if (error.value) {
      console.log("Could not fetch graphs", error);
    }
    fetching.value = isFetching.value;
    if (data.value) {
      graphs.value = data.value.graphs;
    }
  }

  getGraphs();

  return { graphs, fetching };
});
