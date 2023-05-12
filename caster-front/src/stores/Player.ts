import { defineStore } from "pinia";
import { type Ref, computed, ref } from "vue";
import { type Scalars, useStreamSubscription } from "@/graphql/graphql";
import type { StreamPoint } from "@/graphql";

export const usePlayerStore = defineStore("player", () => {
  const micActive: Ref<boolean> = ref(false);
  const play: Ref<boolean> = ref(false);
  const startingTimestamp: Ref<number> = ref(0);
  const playerState: Ref<"start" | "playing" | "end"> = ref("start");

  const graphUuid: Ref<Scalars["UUID"] | undefined> = ref(undefined);

  const { data: streamInfo } = useStreamSubscription({
    pause: computed(() => graphUuid.value === undefined),
    variables: { graphUuid }
  });

  const activeStreamPoint: Ref<StreamPoint | undefined> = ref(undefined);

  const streamGPS: Ref<boolean> = ref(false);

  return {
    micActive,
    play,
    streamInfo,
    graphUuid,
    activeStreamPoint,
    streamGPS,
    startingTimestamp,
    playerState
  };
});
