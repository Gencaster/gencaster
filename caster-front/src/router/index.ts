import { createRouter, createWebHistory } from "vue-router";
import GraphDetail from "@/components/GraphDetail.vue";
import DebugPlayer from "@/components/DebugPlayer.vue";
import Graphs from "@/components/Graphs.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: Graphs
    },
    {
      path: "/debug",
      name: "debug",
      component: DebugPlayer
    },
    {
      path: "/listen/:graphSlug/",
      name: "graphPlayer",
      component: GraphDetail,
      props: route => ({
        graphSlug: route.params.graphSlug,
        fullView: false
      })
    }
  ]
});

export default router;
