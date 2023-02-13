import { createRouter, createWebHistory } from "vue-router";
import GraphView from "@/views/GraphView.vue";
import GraphsView from "@/views/GraphsView.vue";
import LandingView from "@/views/LandingView.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "landing",
      component: LandingView,
    },
    {
      path: "/graphs",
      name: "graphs",
      component: GraphsView,
    },
    {
      path: "/graph/:uuid",
      name: "graph",
      component: GraphView,
    },
  ],
});

export default router;
