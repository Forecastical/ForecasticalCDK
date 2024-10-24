<template>
  <div id="app">
    <NavBar />
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'  // Note: using relative path

export default {
  name: "App",
  components: {
    NavBar
  }
};
</script>

<style>
body {
  margin: 0;
  padding: 0;
  background-color: #1e1e1e;
  min-height: 100vh;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #ffffff;
}

.main-content {
  padding: 20px;
}
</style>