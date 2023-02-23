import { defineStore } from "pinia";
import { type Ref, ref } from "vue";
import type { StreamPointsQuery } from "@/graphql/graphql";
import { useStreamPointsQuery } from "@/graphql/graphql";

export const useStreamPointsStore = defineStore("streamPoints", () => {
  const { data: streamPoints, fetching, error } = useStreamPointsQuery();
  const selectedStreamPoint: Ref<StreamPointsQuery["streamPoints"][0] | undefined> = ref(undefined);

  return {
    streamPoints,
    fetching,
    error,
    selectedStreamPoint
  };
});
