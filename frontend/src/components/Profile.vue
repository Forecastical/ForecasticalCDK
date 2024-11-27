<template>
  <div class="weather-app">
    <div v-if="loading" class="loading">
      Loading user data...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else-if="userData" class="content">
      <div class="left-column">
        <div class="profile-card">
          <h2>Profile Information</h2>
          <div class="profile-info">
            <img src="../assets/hurricane.webp" alt="Profile" class="profile-image" />
            <div class="profile-details">
              <h3>{{ userData.user_fname }} {{ userData.user_lname }}</h3>
              <p class="subtitle">Weather Enthusiast</p>
            </div>
          </div>
        </div>

        <div class="stats-card">
          <h2>Weather Preferences</h2>
          <div class="stats-grid">
            <div class="stat-item">
              <h4>Preferred Temperature</h4>
              <p>{{ userData.preferredTemp }}°{{ userData.use_celsius ? 'C' : 'F' }}</p>
            </div>
            <div class="stat-item">
              <h4>Home Location</h4>
              <p>{{ userData.home || 'Not set' }}</p>
            </div>
            <div class="stat-item">
              <h4>Weather Alerts</h4>
              <p>{{ userData.user_alerts ? 'Enabled' : 'Disabled' }}</p>
            </div>
            <div class="stat-item">
              <h4>Units</h4>
              <p>{{ userData.use_celsius ? 'Celsius' : 'Fahrenheit' }}</p>
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
            <p>{{ userData.user_age }}</p>
          </div>
          <div class="detail-item">
            <strong>Location:</strong>
            <p>{{ userData.home || 'Not set' }}</p>
          </div>
        </div>

        <div class="actions">
          <button @click="updateLocation" class="update-btn" :disabled="loading">
            <span class="icon">↻</span>
            {{ loading ? 'Updating Location...' : 'Update Location' }}
          </button>
          <button @click="openProfileEditor" class="edit-btn" :disabled="loading">
            <span class="icon">✎</span>
            Edit Profile
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <div v-if="showEditModal" class="modal" @click="closeProfileEditor">
      <div class="modal-content" @click.stop>
        <h2>Edit Profile</h2>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <div class="edit-form">
          <div class="form-section">
            <h3>Basic Information</h3>
            
            <div class="form-group">
              <label>First Name:</label>
              <input 
                type="text" 
                v-model="editForm.user_fname"
                placeholder="Enter first name"
              >
            </div>

            <div class="form-group">
              <label>Last Name:</label>
              <input 
                type="text" 
                v-model="editForm.user_lname"
                placeholder="Enter last name"
              >
            </div>

            <div class="form-group">
              <label>Age:</label>
              <input 
                type="number" 
                v-model="editForm.age"
                placeholder="Enter age"
                min="0"
              >
            </div>

            <div class="form-group">
              <label>Location:</label>
              <div class="location-display">
                <span v-if="editForm.home_lat && editForm.home_lon">
                  Lat: {{ editForm.home_lat.toFixed(4) }}, 
                  Lon: {{ editForm.home_lon.toFixed(4) }}
                </span>
                <span v-else>Location not set</span>
                <button 
                  type="button" 
                  @click="updateLocation" 
                  class="location-btn"
                  :disabled="loading"
                >
                  Get Current Location
                </button>
              </div>
            </div>
          </div>

          <div class="form-section">
            <h3>Weather Preferences</h3>
            
            <div class="form-group">
              <label>Preferred Temperature:</label>
              <div class="temperature-input">
                <input 
                  type="number" 
                  v-model="editForm.preferredTemp"
                  placeholder="Enter preferred temperature"
                >
                <span>°{{ editForm.use_celsius ? 'C' : 'F' }}</span>
              </div>
            </div>

            <div class="form-group">
              <label>Weather Alerts:</label>
              <div class="toggle-input">
                <input 
                  type="checkbox"
                  v-model="editForm.user_alerts"
                  id="alertsToggle"
                >
                <label for="alertsToggle">
                  {{ editForm.user_alerts ? 'Enabled' : 'Disabled' }}
                </label>
              </div>
            </div>

            <div class="form-group">
              <label>Temperature Units:</label>
              <div class="toggle-input">
                <input 
                  type="checkbox"
                  v-model="editForm.use_celsius"
                  id="unitsToggle"
                >
                <label for="unitsToggle">
                  {{ editForm.use_celsius ? 'Celsius' : 'Fahrenheit' }}
                </label>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-actions">
          <button 
            @click="saveChanges" 
            class="save-btn" 
            :disabled="loading"
          >
            {{ loading ? 'Saving...' : 'Save Changes' }}
          </button>
          <button 
            @click="closeProfileEditor" 
            class="cancel-btn" 
            :disabled="loading"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
//import { useAuthStore } from '@/store/auth';
import { authService } from '@/services/authService';

export default {
  name: "ProfileView",
  
  data() {
    return {
      showEditModal: false,
      loading: false,
      error: null,
      userData: null,
      editForm: {
        username: "",
        password: "",
        user_fname: "",
        user_lname: "",
        age: null,
        home_lat: null,
        home_lon: null,
        preferredTemp: null,
        use_celsius: false,
        user_alerts: false
      }
    };
  },

  methods: {
    async fetchUserData() {
      try {
        const currentUser = authService.getCurrentUser();
        if (!currentUser) {
          this.error = 'No user data found';
          return;
        }

        this.userData = {
          ...currentUser,
          // Set display values
          alerts: currentUser.user_alerts ? "Enabled" : "Disabled",
          units: currentUser.use_celsius ? "Celsius" : "Fahrenheit",
          // Format location
          home: currentUser.home_lat && currentUser.home_lon 
            ? `${currentUser.home_lat.toFixed(2)}°, ${currentUser.home_lon.toFixed(2)}°` 
            : "Location not set",
          // Ensure we use user_age consistently
          age: currentUser.user_age // This is for backward compatibility
        };

        console.log('Current user data:', this.userData);

      } catch (error) {
        console.error('Error fetching user data:', error);
        this.error = 'Failed to load user data';
      }
    },

    initProfileForm() {
      const currentUser = authService.getCurrentUser();
      if (!currentUser) return;

      console.log('Current user for form init:', currentUser);

      this.editForm = {
        username: currentUser.username,
        password: currentUser.password,
        user_fname: currentUser.user_fname || '',
        user_lname: currentUser.user_lname || '',
        age: currentUser.user_age?.toString() || '', // Using user_age here
        home_lat: currentUser.home_lat,
        home_lon: currentUser.home_lon,
        use_celsius: Boolean(currentUser.use_celsius),
        user_alerts: Boolean(currentUser.user_alerts),
        preferredTemp: currentUser.preferredTemp || ''
      };

      console.log('Initialized edit form:', this.editForm);
    },

    async saveChanges() {
      this.loading = true;
      this.error = null;

      try {
        console.log('Original edit form:', this.editForm);

        const updateData = {
          user_fname: this.editForm.user_fname?.trim() || undefined,
          user_lname: this.editForm.user_lname?.trim() || undefined,
          user_age: this.editForm.age ? parseInt(this.editForm.age) : undefined,
          home_lat: this.editForm.home_lat ? parseFloat(this.editForm.home_lat) : undefined,
          home_lon: this.editForm.home_lon ? parseFloat(this.editForm.home_lon) : undefined,
          use_celsius: this.editForm.use_celsius,
          user_alerts: this.editForm.user_alerts
        };

        // Remove undefined values
        const cleanedData = Object.fromEntries(
          Object.entries(updateData).filter(entry => entry[1] !== undefined)
        );

        console.log('Cleaned update data:', cleanedData);

        await authService.updateUser(cleanedData);
        await this.fetchUserData();
        this.closeProfileEditor();

      } catch (error) {
        console.error('Error updating profile:', error);
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },

    async updateLocation() {
      if (!navigator.geolocation) {
        this.error = 'Geolocation is not supported by your browser';
        return;
      }

      try {
        const position = await new Promise((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(resolve, reject);
        });

        this.editForm.home_lat = position.coords.latitude;
        this.editForm.home_lon = position.coords.longitude;

        // If we're not in edit mode, open the editor
        if (!this.showEditModal) {
          this.openProfileEditor();
        }

      } catch (error) {
        console.error('Error getting location:', error);
        this.error = 'Could not get your location';
      }
    },

    openProfileEditor() {
      this.initProfileForm();
      this.showEditModal = true;
      this.error = null;
    },

    closeProfileEditor() {
      this.showEditModal = false;
      this.error = null;
    }
  },

  mounted() {
    this.fetchUserData();
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

.toggle-input {
  display: flex;
  align-items: center;
  gap: 10px;
}

.toggle-input input[type="checkbox"] {
  width: auto;
  margin-right: 8px;
}

.temperature-input {
  display: flex;
  align-items: center;
  gap: 8px;
}

.temperature-input input {
  flex: 1;
}

.temperature-input span {
  color: #bdc3c7;
  font-size: 0.9em;
}

.location-display {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  color: #bdc3c7;
}

.location-btn {
  padding: 4px 8px;
  font-size: 0.9em;
  background-color: #3498db;
  white-space: nowrap;
}

.loading {
  text-align: center;
  padding: 40px;
  background-color: #34495e;
  border-radius: 10px;
  margin: 20px;
  color: #50e2e7;
}

.error {
  text-align: center;
  padding: 20px;
  background-color: rgba(231, 76, 60, 0.2);
  border-radius: 10px;
  margin: 20px;
  color: #e74c3c;
}

.error-message {
  background-color: rgba(231, 76, 60, 0.2);
  color: #e74c3c;
  padding: 12px;
  border-radius: 5px;
  margin-bottom: 20px;
}
</style>
