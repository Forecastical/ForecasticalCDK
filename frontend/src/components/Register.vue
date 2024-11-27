<!-- src/components/Register.vue -->
<template>
    <div class="register-container">
      <div class="register-card">
        <h2>Create Account</h2>
        <p class="subtitle">Join Forecastical today</p>
        
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label for="username">Username</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              placeholder="Choose a username"
            />
          </div>
  
          <div class="form-group">
            <label for="password">Password</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              placeholder="Choose a password"
            />
          </div>
  
          <div class="form-row">
            <div class="form-group">
              <label for="firstName">First Name</label>
              <input
                id="firstName"
                v-model="form.firstName"
                type="text"
                required
                placeholder="First name"
              />
            </div>
            
            <div class="form-group">
              <label for="lastName">Last Name</label>
              <input
                id="lastName"
                v-model="form.lastName"
                type="text"
                required
                placeholder="Last name"
              />
            </div>
          </div>
  
          <div class="form-row">
            <div class="form-group">
              <label for="age">Age</label>
              <input
                id="age"
                v-model.number="form.age"
                type="number"
                required
                min="13"
                placeholder="Your age"
              />
            </div>
          </div>
  
          <div class="form-group">
            <label for="location">Default Location</label>
            <button type="button" @click="getCurrentLocation" class="location-btn">
              {{ locationLoading ? 'Getting location...' : 'Use My Location' }}
            </button>
            <div class="location-display" v-if="form.latitude && form.longitude">
              Lat: {{ form.latitude }}, Lon: {{ form.longitude }}
            </div>
          </div>
  
          <div class="form-row">
            <div class="form-group checkbox">
              <label>
                <input
                  type="checkbox"
                  v-model="form.useCelsius"
                />
                Use Celsius
              </label>
            </div>
  
            <div class="form-group checkbox">
              <label>
                <input
                  type="checkbox"
                  v-model="form.enableAlerts"
                />
                Enable Weather Alerts
              </label>
            </div>
          </div>
  
          <div v-if="error" class="error-message">
            {{ error }}
          </div>
  
          <button type="submit" class="register-btn" :disabled="loading">
            {{ loading ? 'Creating Account...' : 'Create Account' }}
          </button>
        </form>
  
        <div class="login-prompt">
          <p>Already have an account?</p>
          <router-link to="/login" class="login-link">Sign in instead</router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '@/store/auth';
  
  export default {
    name: 'RegisterForm',
    
    setup() {
      const router = useRouter();
      const auth = useAuthStore();
      
      const form = reactive({
        username: '',
        password: '',
        firstName: '',
        lastName: '',
        age: null,
        latitude: null,
        longitude: null,
        useCelsius: false,
        enableAlerts: true
      });
  
      const error = ref('');
      const loading = ref(false);
      const locationLoading = ref(false);
  
      const getCurrentLocation = () => {
        locationLoading.value = true;
        
        navigator.geolocation.getCurrentPosition(
          (position) => {
            form.latitude = position.coords.latitude;
            form.longitude = position.coords.longitude;
            locationLoading.value = false;
          },
          (err) => {
            console.error('Geolocation error:', err);
            error.value = 'Failed to get location. Please try again.';
            locationLoading.value = false;
          }
        );
      };
  
      const handleRegister = async () => {
        if (!form.latitude || !form.longitude) {
          error.value = 'Please set your location';
          return;
        }
  
        loading.value = true;
        error.value = '';
  
        try {
          await auth.register(form);
          // After successful registration, navigate to login
          router.push('/login');
        } catch (err) {
          error.value = err.response?.data?.message || 'Failed to create account. Please try again.';
        } finally {
          loading.value = false;
        }
      };
  
      return {
        form,
        error,
        loading,
        locationLoading,
        getCurrentLocation,
        handleRegister
      };
    }
  };
  </script>
  
  <style scoped>
  .register-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background-color: #1e1e1e;
  }
  
  .register-card {
    background-color: #34495e;
    padding: 40px;
    border-radius: 10px;
    width: 100%;
    max-width: 500px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  h2 {
    color: #50e2e7;
    text-align: center;
    margin: 0 0 10px 0;
  }
  
  .subtitle {
    color: #bdc3c7;
    text-align: center;
    margin-bottom: 30px;
  }
  
  .register-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .form-row {
    display: flex;
    gap: 20px;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
  }
  
  .form-group.checkbox {
    flex-direction: row;
    align-items: center;
  }
  
  label {
    color: #50e2e7;
    font-size: 0.9em;
  }
  
  input:not([type="checkbox"]) {
    padding: 12px;
    border: 1px solid #405468;
    border-radius: 5px;
    background-color: #2c3e50;
    color: white;
    font-size: 1em;
  }
  
  input:focus {
    outline: none;
    border-color: #50e2e7;
  }
  
  .location-btn {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .location-btn:hover {
    background-color: #2980b9;
  }
  
  .location-display {
    color: #bdc3c7;
    font-size: 0.9em;
    margin-top: 5px;
  }
  
  .register-btn {
    background-color: #50e2e7;
    color: #1e1e1e;
    border: none;
    padding: 12px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
    font-weight: bold;
    transition: background-color 0.3s ease;
  }
  
  .register-btn:hover:not(:disabled) {
    background-color: #3dd8dd;
  }
  
  .register-btn:disabled {
    background-color: #597ea2;
    cursor: not-allowed;
  }
  
  .error-message {
    color: #ff6b6b;
    font-size: 0.9em;
    text-align: center;
    padding: 8px;
    background-color: rgba(255, 107, 107, 0.1);
    border-radius: 4px;
  }
  
  .login-prompt {
    margin-top: 30px;
    text-align: center;
    color: #bdc3c7;
  }
  
  .login-link {
    color: #50e2e7;
    text-decoration: none;
    font-weight: bold;
  }
  
  .login-link:hover {
    text-decoration: underline;
  }
  
  @media (max-width: 600px) {
    .form-row {
      flex-direction: column;
      gap: 20px;
    }
    
    .register-card {
      padding: 20px;
    }
  }
  </style>