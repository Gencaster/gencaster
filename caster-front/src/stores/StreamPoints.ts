import { defineStore } from "pinia";
import { type Ref, computed, ref } from "vue";
import { type Scalars, type StreamPoint, useGetGraphsQuery, useStreamPointsQuery, useStreamSubscription } from "@/graphql/graphql";

export const useStreamPointStore = defineStore("streamPoints", () => {
  const activeStreamPoint: Ref<StreamPoint> = ref({} as StreamPoint);
  const micActive: Ref<boolean> = ref(false);
  const play: Ref<boolean> = ref(false);
  const selectedGraphUuid: Ref<Scalars["UUID"] | undefined> = ref(undefined);

  const { data: streamPoints, fetching, error } = useStreamPointsQuery();

  const { data: graphs } = useGetGraphsQuery();

  const { data: streamInfo } = useStreamSubscription({
    pause: computed(() => selectedGraphUuid.value === undefined),
    variables: { graphUuid: selectedGraphUuid }
  });

  return {
    streamPoints,
    streamInfo,
    fetching,
    error,
    play,
    activeStreamPoint,
    micActive,
    selectedGraphUuid,
    graphs
  };
});
