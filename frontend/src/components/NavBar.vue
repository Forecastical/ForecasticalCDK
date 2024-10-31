<template>
    <nav class="navbar">
      <div class="nav-content">
        <router-link to="/" class="nav-brand">Forecastical</router-link>
        <div class="nav-links">
          <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">
            <span class="icon">🏠</span>
            Weather
          </router-link>
          <router-link to="/profile" class="nav-link" :class="{ active: $route.path === '/profile' }">
            <span class="icon">👤</span>
            Profile
          </router-link>
          <router-link to="/feed" class="nav-link" :class="{ active: $route.path === '/feed' }">
            <span class="icon">📷</span>
            Feed
        </router-link>
        <router-link to="/recommendations" class="nav-link" :class="{ active: $route.path === '/recommendations' }">
            <span class="icon">🎯</span>
            Recommendations
        </router-link>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'NavBar'
  }
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
  </style>