import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import AdminView from "@/views/AdminView.vue";
import GraphPlayerView from "@/views/GraphPlayerView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView
    },
    {
      path: "/admin",
      name: "admin",
      component: AdminView
    },
    {
      path: "/graph/:graphUuid/player",
      name: "graphPlayer",
      component: GraphPlayerView
    }

  ]
});

export default router;
