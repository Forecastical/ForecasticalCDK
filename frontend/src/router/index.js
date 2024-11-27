import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from '@/store/auth';
import WeatherApp from "@/components/WeatherApp.vue";
import Profile from "@/components/Profile.vue";
import WeatherFeed from "@/components/WeatherFeed.vue";
import WeatherRecommendations from "@/components/WeatherRecommendations.vue";
import WeatherApiTest from "@/components/WeatherApiTest.vue";
import InteractiveHub from "@/components/InteractiveHub.vue";
import LoginForm from "@/components/Login.vue";
import RegisterForm from "@/components/Register.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: WeatherApp,
  },
  {
    path: "/login",
    name: "Login",
    component: LoginForm,
  },
  {
    path: "/register",
    name: "Register",
    component: RegisterForm,
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
    path: "/test",
    name: "ApiTest",
    component: WeatherApiTest,
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

// Add the navigation guard after creating the router
router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/register'];
  const authRequired = !publicPages.includes(to.path);
  const auth = useAuthStore();

  if (authRequired && !auth.isAuthenticated) {
    return next('/login');
  }
  next();
});

export default router;