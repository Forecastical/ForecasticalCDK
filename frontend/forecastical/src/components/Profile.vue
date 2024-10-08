<template>
  <div class="weather-app">
    <header>
      <h1>Profile</h1>
      <router-link to="/">Go to Weather</router-link>
    </header>
    <div class="content">
      <div class="left-column">
        <div class="current-weather">
          <img src="../assets/hurricane.webp" alt="" class="profile img" />
          <p>Beep beep boop boop</p>
        </div>

        <div class="update-location">
          <button @click="updateLocation">
            <span class="icon">↻</span>
            Update Location
          </button>
        </div>
      </div>
      <div class="right-column">
        <div class="supplementary-conditions">
          <h2>Profile</h2>
          <p>Username: {{ username }}</p>
          <p>Age: {{ age }}</p>
          <p>Gender: {{ gender }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfileName",
  data() {
    return {
      username: "Prof. ShuaiXu",
      age: 38,
      home: "Cuyahoga County",
    };
  },
  methods: {
    //
  },
  computed: {
    //
  },
};
</script>

<style scoped>
.weather-app {
  font-family: Arial, sans-serif;
  color: white;
  background-color: #1e1e1e;
  padding: 20px;
  border-radius: 10px;
}

header {
  background-color: #50e2e7;
  padding: 10px;
  text-align: center;
  border-radius: 5px;
}

.content {
  display: flex;
  margin-top: 20px;
}

.left-column {
  flex: 3;
  margin-right: 20px;
}

.right-column {
  flex: 1;
}

.update-location,
.current-weather,
.today-forecast,
.weekly-forecast,
.supplementary-conditions,
.updated-user-forecast {
  background-color: #34495e;
  padding: 15px;
  margin-bottom: 20px;
  border-radius: 5px;
}

.update-location button {
  background-color: #3498db;
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.weather-icon {
  font-size: 2em;
}

h2 {
  margin-top: 0;
}

.profile {
  width: 200px;
  height: 200px;
}
</style>
