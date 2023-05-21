import { defineStore } from "pinia";
import { type Ref, ref } from "vue";
import type { Scalars, StreamPoint } from "@/graphql";
import { PlayerState } from "@/models";

export const usePlayerStore = defineStore("player", () => {
  const micActive: Ref<boolean> = ref(false);
  const play: Ref<boolean> = ref(false);
  const startingTimestamp: Ref<number> = ref(0);
  const playerState: Ref<PlayerState> = ref(PlayerState.Start);
  const graphUuid: Ref<Scalars["UUID"] | undefined> = ref(undefined);

  // const { data: streamInfo } = useStreamSubscription({
  //   pause: computed(() => graphUuid.value === undefined),
  //   variables: { graphUuid }
  // });

  const activeStreamPoint: Ref<StreamPoint | undefined> = ref(undefined);

  const streamGPS: Ref<boolean> = ref(false);
  const gpsError: Ref<GeolocationPositionError | undefined> = ref(undefined);
  const gpsSuccess: Ref<boolean | undefined> = ref(undefined);

  return {
    micActive,
    play,
    graphUuid,
    activeStreamPoint,
    streamGPS,
    startingTimestamp,
    playerState,
    gpsError,
    gpsSuccess,
  };
});
