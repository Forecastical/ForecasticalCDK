<template>
  <div class="weather-app">
    <div class="content">
      <div class="left-column">
        <div class="profile-card">
          <h2>Profile Information</h2>
          <div class="profile-info">
            <img src="../assets/hurricane.webp" alt="Profile" class="profile-image" />
            <div class="profile-details">
              <h3>{{ username }}</h3>
              <p class="subtitle">Weather Enthusiast</p>
            </div>
          </div>
        </div>
        <div class="stats-card">
          <h2>Weather Preferences</h2>
          <div class="stats-grid">
            <div class="stat-item">
              <h4>Preferred Temperature</h4>
              <p>72°F</p>
            </div>
            <div class="stat-item">
              <h4>Home Location</h4>
              <p>{{ home }}</p>
            </div>
            <div class="stat-item">
              <h4>Weather Alerts</h4>
              <p>Enabled</p>
            </div>
            <div class="stat-item">
              <h4>Units</h4>
              <p>Fahrenheit</p>
            </div>
          </div>
        </div>
      </div>
      <div class="right-column">
        <div class="user-details">
          <h2>Account Details</h2>
          <div class="detail-item">
            <strong>Username:</strong>
            <p>{{ username }}</p>
          </div>
          <div class="detail-item">
            <strong>Age:</strong>
            <p>{{ age }}</p>
          </div>
          <div class="detail-item">
            <strong>Location:</strong>
            <p>{{ home }}</p>
          </div>
        </div>
        <div class="actions">
          <button @click="updateLocation" class="update-btn">
            <span class="icon">↻</span>
            Update Location
          </button>
          <button class="edit-btn">
            <span class="icon">✎</span>
            Edit Profile
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfileView",
  data() {
    return {
      username: "Prof. ShuaiXu",
      age: 38,
      home: "Cuyahoga County",
    };
  },
  methods: {
    updateLocation() {
      // Implement location update logic
      console.log("Updating location...");
    }
  }
};
</script>

<style scoped>
.weather-app {
  font-family: Arial, sans-serif;
  color: white;
  background-color: #1e1e1e;
  padding: 0 20px 20px 20px; /* Add this line */
  border-radius: 10px;
  max-width: 1200px;
  margin: 0 auto;
}

.content {
  display: flex;
  gap: 20px;
}

.left-column {
  flex: 3;
}

.right-column {
  flex: 1;
}

.profile-card, .stats-card, .user-details {
  background-color: #34495e;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 5px;
}

.profile-info {
  display: flex;
  align-items: center;
  margin: 20px 0;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #50e2e7;
}

.profile-details {
  margin-left: 20px;
}

.profile-details h3 {
  margin: 0;
  font-size: 1.8em;
  color: #50e2e7;
}

.subtitle {
  color: #bdc3c7;
  margin: 5px 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 15px;
}

.stat-item {
  text-align: center;
  padding: 15px;
  background-color: #2c3e50;
  border-radius: 5px;
}

.stat-item h4 {
  color: #50e2e7;
  margin: 0 0 10px 0;
}

.stat-item p {
  margin: 0;
  font-size: 1.2em;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #455d7a;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-item strong {
  color: #50e2e7;
}

.detail-item p {
  margin: 0;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

button {
  width: 100%;
  background-color: #3498db;
  border: none;
  color: white;
  padding: 12px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

button:hover {
  background-color: #2980b9;
}

.edit-btn {
  background-color: #2ecc71;
}

.edit-btn:hover {
  background-color: #27ae60;
}

h2 {
  color: #50e2e7;
  margin-top: 0;
  margin-bottom: 20px;
}

.icon {
  font-size: 1.2em;
}
</style>