import { defineStore } from "pinia";
import type { Ref } from "vue";
import { ref } from "vue";
import { type StreamPoint, useStreamPointsQuery, useStreamSubscription } from "@/graphql/graphql";

export const useStreamPointStore = defineStore("streamPoints", () => {
  const activeStreamPoint: Ref<StreamPoint> = ref({} as StreamPoint);
  const micActive: Ref<boolean> = ref(false);
  const play: Ref<boolean> = ref(false);

  const { data: streamPoints, fetching, error } = useStreamPointsQuery();

  const { data: streamInfo } = useStreamSubscription();

  return {
    streamPoints,
    streamInfo,
    fetching,
    error,
    play,
    activeStreamPoint,
    micActive
  };
});
