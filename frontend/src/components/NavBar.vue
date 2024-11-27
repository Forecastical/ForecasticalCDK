<template>
  <nav class="navbar">
    <div class="nav-content">
      <router-link to="/" class="nav-brand">Forecastical</router-link>
      <div class="nav-links">
        <router-link
          to="/"
          class="nav-link"
          :class="{ active: $route.path === '/' }"
        >
          <span class="icon">🏠</span>
          Weather
        </router-link>
        
        <!-- Only show these links if user is authenticated -->
        <template v-if="auth.isAuthenticated">
          <router-link
            to="/profile"
            class="nav-link"
            :class="{ active: $route.path === '/profile' }"
          >
            <span class="icon">👤</span>
            Profile
          </router-link>
          <router-link
            to="/feed"
            class="nav-link"
            :class="{ active: $route.path === '/feed' }"
          >
            <span class="icon">📷</span>
            Feed
          </router-link>
          <router-link
            to="/recommendations"
            class="nav-link"
            :class="{ active: $route.path === '/recommendations' }"
          >
            <span class="icon">🎯</span>
            Recommendations
          </router-link>
          <router-link
            to="/test"
            class="nav-link"
            :class="{ active: $route.path === '/test' }"
          >
            <span class="icon">🔧</span>
            API Test
          </router-link>
          <router-link
            to="/hub"
            class="nav-link"
            :class="{ active: $route.path === '/hub' }"
          >
            <span class="icon">🔧</span>
            Interactive Hub
          </router-link>
          
          <!-- Logout button -->
          <button @click="handleLogout" class="nav-link logout-btn">
            <span class="icon">🚪</span>
            Logout
          </button>
        </template>

        <!-- Show login button when not authenticated -->
        <template v-else>
          <router-link
            to="/login"
            class="nav-link"
            :class="{ active: $route.path === '/login' }"
          >
            <span class="icon">🔑</span>
            Login
          </router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script>
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';

export default {
  name: "NavBar",
  setup() {
    const auth = useAuthStore();
    const router = useRouter();

    const handleLogout = () => {
      auth.logout();
      router.push('/login');
    };

    return {
      auth,
      handleLogout
    };
  }
};
</script>

<style scoped>
.navbar {
  background-color: #34495e;
  padding: 0.5rem;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.nav-brand {
  color: #50e2e7;
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background-color: #2c3e50;
  color: #50e2e7;
}

.nav-link.active {
  background-color: #50e2e7;
  color: #1e1e1e;
}

.icon {
  font-size: 1.2rem;
}

.logout-btn {
  background: none;
  border: none;
  font-family: inherit;
  font-size: inherit;
  cursor: pointer;
  padding: 8px 16px;
  color: white;
  display: flex;
  align-items: center;
  gap: 8px;
}

.logout-btn:hover {
  background-color: #2c3e50;
  color: #50e2e7;
}
</style>
