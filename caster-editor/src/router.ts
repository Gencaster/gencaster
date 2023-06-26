import { createRouter, createWebHistory } from "vue-router";
import GraphDetailView from "@/views/GraphDetailView.vue";
import GraphsView from "@/views/GraphsView.vue";
import LandingView from "@/views/LandingView.vue";

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
      path: "/graph/:uuid",
      name: "graph",
      component: GraphDetailView,
    },
  ],
});

export default router;
