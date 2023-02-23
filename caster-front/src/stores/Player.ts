import { defineStore } from "pinia";
import { type Ref, computed, ref } from "vue";
import { type Scalars, useStreamSubscription } from "@/graphql/graphql";
import type { StreamPoint } from "@/graphql";

export const usePlayerStore = defineStore("player", () => {
  const micActive: Ref<boolean> = ref(false);
  const play: Ref<boolean> = ref(false);

  const graphUuid: Ref<Scalars["UUID"] | undefined> = ref(undefined);

  const { data: streamInfo } = useStreamSubscription({
    pause: computed(() => graphUuid.value === undefined),
    variables: { graphUuid }
  });

  const activeStreamPoint: Ref<StreamPoint | undefined> = ref(undefined);

  return {
    micActive,
    play,
    streamInfo,
    graphUuid,
    activeStreamPoint
  };
});
