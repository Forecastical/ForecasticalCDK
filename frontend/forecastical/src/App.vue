<template>
  <div id="app">
    <NavBar />
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'  // uses relative path

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
  display: flex;
  flex-direction: column;
  align-items: center;
  .masonry-container {
    padding: 0.5rem 0;
    @media (max-width: 540px) {
      width: 100% !important;
      padding: 1rem;
    }
    > .md-card {
      max-width: 250px;
      margin: 0.5rem;
      @media (min-width: 1500px) {
        max-width: 300px;
      }
      @media (max-width: 540px) {
        max-width: 100%;
      }
    }
  }
}
.main-content {
  padding: 20px;
}

</style>
