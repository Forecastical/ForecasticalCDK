<template>
  <div class="weather-app">
    <div class="content">

      <div class="left-column">

        <div class="profile-card">
          <h2>Profile Information</h2>
          <div class="profile-info">
            <img src="../assets/hurricane.webp" alt="Profile" class="profile-image" />
            <div class="profile-details">
              <h3>{{ userData.username }}</h3>
              <p class="subtitle">Weather Enthusiast</p>
            </div>
          </div>
        </div>

        <div class="stats-card">
          <h2>Weather Preferences</h2>
          <div class="stats-grid">
            <div class="stat-item">
              <h4>Preferred Temperature</h4>
              <p>{{ userData.preferredTemp }}°F</p>
            </div>
            <div class="stat-item">
              <h4>Home Location</h4>
              <p>{{ userData.home }}</p>
            </div>
            <div class="stat-item">
              <h4>Weather Alerts</h4>
              <p>{{ userData.alerts }}</p>
            </div>
            <div class="stat-item">
              <h4>Units</h4>
              <p>{{ userData.units }}</p>
            </div>
          </div>
        </div>

      </div>

      <div class="right-column">

        <div class="user-details">
          <h2>Account Details</h2>
          <div class="detail-item">
            <strong>Username:</strong>
            <p>{{ userData.username }}</p>
          </div>
          <div class="detail-item">
            <strong>Age:</strong>
            <p>{{ userData.age }}</p>
          </div>
          <div class="detail-item">
            <strong>Location:</strong>
            <p>{{ userData.home }}</p>
          </div>
        </div>

        <div class="actions">
          <button @click="updateLocation" class="update-btn">
            <span class="icon">↻</span>
            Update Location
          </button>
          <button @click="openProfileEditor" class="edit-btn">
            <span class="icon">✎</span>
            Edit Profile
          </button>
        </div>

      </div>

    </div>

    <!--Editing profile form-->
    <div v-if="showEditModal" class="modal" @click="closeProfileEditor">
      <div class="modal-content" @click.stop>
        <h2>Edit Profile</h2>
        
        <div class="edit-form">
          <div class="form-section">

            <h3>Basic Information</h3>
            <div class="form-group">
              <label>Username:</label>
              <input 
                type="text" 
                v-model="editForm.username"
                placeholder="Enter username"
              >
            </div>

            <div class="form-group">
              <label>Age:</label>
              <input 
                type="number" 
                v-model="editForm.age"
                placeholder="Enter age"
              >
            </div>

            <div class="form-group">
              <label>Location:</label>
              <input 
                type="text" 
                v-model="editForm.home"
                placeholder="Enter location"
              >
            </div>

          </div>

          <div class="form-section">
            <h3>Weather Preferences</h3>
            <div class="form-group">
              <label>Preferred Temperature (°F):</label>
              <input 
                type="number" 
                v-model="editForm.preferredTemp"
                placeholder="Enter preferred temperature"
              >
            </div>

            <div class="form-group">
              <label>Weather Alerts:</label>
              <select v-model="editForm.alerts">
                <option value="Enabled">Enabled</option>
                <option value="Disabled">Disabled</option>
              </select>
            </div>

            <div class="form-group">
              <label>Units:</label>
              <select v-model="editForm.units">
                <option value="Fahrenheit">Fahrenheit</option>
                <option value="Celsius">Celsius</option>
              </select>
            </div>
          </div>
        </div>

        <div class="modal-actions">
          <button @click="saveChanges" class="save-btn">
            Save Changes
          </button>
          <button @click="closeProfileEditor" class="cancel-btn">
            Cancel
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
      showEditModal: false,
      
      userData: {
        username: "Prof. ShuaiXu",
        age: 38,
        home: "Cuyahoga County",
        preferredTemp: 72,
        alerts: "Enabled",
        units: "Fahrenheit"
      },
      
      editForm: {
        username: "",
        age: null,
        home: "",
        preferredTemp: null,
        alerts: "",
        units: ""
      }
    };
  },

  methods: {
    openProfileEditor() {
      this.initProfileForm();
      this.showEditModal = true;
    },

    closeProfileEditor() {
      this.showEditModal = false;
    },

    // initialize form with the current user data
    initProfileForm() {
      this.editForm = { ...this.userData };
    },

    saveChanges() {
      this.userData = { ...this.editForm };
      this.closeProfileEditor();
    },

    updateLocation() {
      console.log("Updating location...");
      // TODO: Implement location update logic
    }
  }
};
</script>

<style scoped>
.weather-app {
  font-family: Arial, sans-serif;
  color: white;
  background-color: #1e1e1e;
  padding: 0 20px 20px 20px;
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
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.edit-btn {
  background-color: #2ecc71;
}

.edit-btn:hover {
  background-color: #27ae60;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #34495e;
  padding: 30px;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
}

.form-section {
  margin-bottom: 30px;
}

.form-section h3 {
  color: #50e2e7;
  margin-bottom: 15px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  color: #50e2e7;
  margin-bottom: 5px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #405468;
  background-color: #2c3e50;
  color: white;
  border-radius: 5px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.save-btn {
  background-color: #2ecc71;
}

.cancel-btn {
  background-color: #e74c3c;
}

.save-btn:hover {
  background-color: #27ae60;
}

.cancel-btn:hover {
  background-color: #c0392b;
}

@media (max-width: 768px) {
  .content {
    flex-direction: column;
  }
  
  .modal-content {
    width: 95%;
    margin: 20px;
    max-height: 90vh;
  }
  
  .form-group input,
  .form-group select {
    font-size: 16px;
  }
}
</style>
