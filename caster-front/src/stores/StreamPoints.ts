import { defineStore } from "pinia";
import type { Ref } from "vue";
import { ref } from "vue";
import { type StreamPoint, useGetStreamPointsQuery } from "@/graphql/graphql";

export const useStreamPointStore = defineStore("streamPoints", () => {
  const streamPoints: Ref<Array<StreamPoint>> = ref([]);
  const fetching: Ref<boolean> = ref(true);
  const activeStreamPoint: Ref<StreamPoint> = ref({} as StreamPoint);
  const micActive: Ref<boolean> = ref(false);
  const play: Ref<boolean> = ref(false);

  const getStreamPoints = async () => {
    const { data, fetching: isFetching, error } = await useGetStreamPointsQuery();
    if (error.value)
      console.log("Error while querying stream points", error);
    fetching.value = isFetching.value;
    if (data.value)
      streamPoints.value = data.value.streamPoints;
  };

  getStreamPoints();

  return {
    streamPoints,
    play,
    activeStreamPoint,
    micActive
  };
});
