import { createRouter, createWebHistory }
from "vue-router";

import DashboardView
from "../views/DashboardView.vue";

import AnalyticsView
from "../views/AnalyticsView.vue";

const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: "/",
      component: DashboardView
    },
    {
      path: "/analytics",
      component: AnalyticsView
    }
  ]
});

export default router;