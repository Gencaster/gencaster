import { createRouter, createWebHistory } from "vue-router";
import GraphDetail from "@/components/GraphDetail.vue";
import DebugPlayer from "@/components/DebugPlayer.vue";
import Graphs from "@/components/GraphsOverview.vue";
import GpsError from "@/components/GpsError.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: Graphs,
    },
    {
      path: "/debug",
      name: "debug",
      component: DebugPlayer,
    },
    {
      path: "/gpsError",
      name: "gpsError",
      component: GpsError,
    },
    {
      path: "/listen/:graphSlug/",
      name: "graphPlayer",
      component: GraphDetail,
      props: route => ({
        graphSlug: route.params.graphSlug,
        fullView: false,
      }),
    },
  ],
});

export default router;
