import { createRouter, createWebHistory } from "vue-router";
import WeatherApp from "@/components/WeatherApp.vue";
import Profile from "@/components/Profile.vue";
import WeatherFeed from "@/components/WeatherFeed.vue";
import WeatherRecommendations from "@/components/WeatherRecommendations.vue";
import InteractiveHub from "@/components/InteractiveHub.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: WeatherApp,
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
  },
  {
    path: "/feed",
    name: "WeatherFeed",
    component: WeatherFeed,
  },
  {
    path: "/recommendations",
    name: "WeatherRecommendations",
    component: WeatherRecommendations,
  },
  {
    path: "/hub",
    name: "InteractiveHub",
    component: InteractiveHub,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
