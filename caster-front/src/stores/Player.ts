import { defineStore } from "pinia";
import { type Ref, computed, ref } from "vue";
import { type Scalars, useStreamSubscription } from "@/graphql/graphql";
import type { StreamPoint } from "@/graphql";
import type { PlayerState, UserDataRequest } from "@/models";

export const usePlayerStore = defineStore("player", () => {
  const micActive: Ref<boolean> = ref(false);
  const play: Ref<boolean> = ref(false);
  const startingTimestamp: Ref<number> = ref(0);
  const playerState: Ref<PlayerState> = ref("start");
  const showInfo: Ref<boolean> = ref(false);

  // gps
  const gpsErrored: Ref<boolean> = ref(false);
  const gpsAllowed: Ref<boolean> = ref(false);

  // popups
  const userDataRequests: Ref<Array<UserDataRequest>> = ref([]);

  // content of the graph
  const title: Ref<string> = ref("Title of Graph");
  const description: Ref<string> = ref("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy.");
  const infoContent: Ref<string> = ref("<h1>Über</h1> <p> Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. </p> <p> Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. </p> <div class=\"block-image\" title=\"Single Image\"> <div> <img src=\"https://placehold.jp/1500x1000.png\" alt=\"\"> </div> </div> <p> Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. </p> <p> Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. </p> <div class=\"block-image\" title=\"Single Image\"> <div> <img src=\"https://placehold.jp/1500x1000.png\" alt=\"\"> </div> </div> <p> Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. </p> <p> Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. </p>");
  const endContent: Ref<string> = ref("<h1>End</h1> <p> Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. </p> <p> Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. </p> <div class=\"block-image\" title=\"Single Image\"> <div> <img src=\"https://placehold.jp/1500x1000.png\" alt=\"\"> </div> </div> <p> Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. </p> <p> Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. </p> <div class=\"block-image\" title=\"Single Image\"> <div> <img src=\"https://placehold.jp/1500x1000.png\" alt=\"\"> </div> </div> <p> Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. </p> <p> Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. </p>");

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
    gpsErrored,
    gpsAllowed,
    startingTimestamp,
    playerState,
    title,
    description,
    infoContent,
    endContent,
    showInfo,
    userDataRequests
  };
});
