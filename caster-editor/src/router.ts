import { createRouter, createWebHistory } from "vue-router";
import GraphDetailView from "@/views/GraphDetailView.vue";
import GraphsView from "@/views/GraphsView.vue";
import LandingView from "@/views/LandingView.vue";
import StreamList from "@/components/StreamList.vue";
import StreamLog from "@/components/StreamLogs.vue";
import StreamPointList from "@/components/StreamPointList.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  // add typescript/enums for paths
  routes: [
    {
      path: "/",
      name: "landing",
      component: LandingView,
    },
    {
      path: "/graph",
      name: "graphs",
      component: GraphsView,
    },
    {
      path: "/stream",
      name: "streams",
      component: StreamList,
    },
    {
      path: "/stream/:uuid/logs",
      name: "streamLogs",
      component: StreamLog,
      props: (route) => ({
        streamUuid: route.params.uuid,
      }),
    },
    {
      path: "/stream-point",
      name: "streamPoints",
      component: StreamPointList,
    },
    {
      path: "/stream-point/:uuid/logs",
      name: "streamPointLogs",
      component: StreamLog,
      props: (route) => ({
        streamPointUuid: route.params.uuid,
      }),
    },
    {
      path: "/graph/:uuid",
      name: "graph",
      component: GraphDetailView,
    },
  ],
});

export default router;
