import { createRouter, createWebHistory } from "vue-router";
import WeatherApp from "@/components/WeatherApp.vue";
import Profile from "@/components/Profile.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: WeatherApp,
  },
  { path: "/profile", name: "Profile", component: Profile },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
