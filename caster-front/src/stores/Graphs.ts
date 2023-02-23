import { defineStore } from "pinia";
import { type Ref, ref } from "vue";
import { type GetGraphsQuery, useGetGraphsQuery } from "@/graphql/graphql";

export const useGraphsStore = defineStore("graphs", () => {
  const selectedGraph: Ref<GetGraphsQuery["graphs"][0] | undefined> = ref(undefined);

  const { data: graphs, fetching } = useGetGraphsQuery();

  return {
    selectedGraph,
    graphs,
    fetching
  };
});
