import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/:user_id/:range(week|month|range)/:year/:interval?",
    name: "Home",
    component: Home,
  },
  { path: "*", redirect: "/1528/week/2022/25" },
];

const router = new VueRouter({
  routes,
});

export default router;
