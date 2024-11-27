<!-- src/components/Login.vue -->
<template>
    <div class="login-container">
      <div class="login-card">
        <h2>Welcome to Forecastical</h2>
        <p class="subtitle">Sign in to continue</p>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="username">Username</label>
            <input
              id="username"
              v-model="username"
              type="text"
              required
              placeholder="Enter your username"
            />
          </div>
  
          <div class="form-group">
            <label for="password">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              placeholder="Enter your password"
            />
          </div>
  
          <div v-if="error" class="error-message">
            {{ error }}
          </div>
  
          <button type="submit" class="login-btn" :disabled="loading">
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>
  
        <div class="register-prompt">
          <p>Don't have an account?</p>
          <router-link to="/register" class="register-link">Create one now</router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '@/store/auth';
  
  export default {
    name: 'LoginForm',
    
    setup() {
      const router = useRouter();
      const auth = useAuthStore();
      
      const username = ref('');
      const password = ref('');
      const error = ref('');
      const loading = ref(false);
  
      const handleLogin = async () => {
        if (!username.value || !password.value) {
          error.value = 'Please enter both username and password';
          return;
        }
  
        loading.value = true;
        error.value = '';
  
        try {
          await auth.login(username.value, password.value);
          router.push('/'); // Redirect to home page after successful login
        } catch (err) {
          error.value = err.response?.data?.message || 'Failed to sign in. Please check your credentials.';
        } finally {
          loading.value = false;
        }
      };
  
      return {
        username,
        password,
        error,
        loading,
        handleLogin
      };
    }
  };
  </script>
  
  <style scoped>
  .login-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background-color: #1e1e1e;
  }
  
  .login-card {
    background-color: #34495e;
    padding: 40px;
    border-radius: 10px;
    width: 100%;
    max-width: 400px;
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
  
  .login-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  label {
    color: #50e2e7;
    font-size: 0.9em;
  }
  
  input {
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
  
  .login-btn {
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
  
  .login-btn:hover:not(:disabled) {
    background-color: #3dd8dd;
  }
  
  .login-btn:disabled {
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
  
  .register-prompt {
    margin-top: 30px;
    text-align: center;
    color: #bdc3c7;
  }
  
  .register-link {
    color: #50e2e7;
    text-decoration: none;
    font-weight: bold;
  }
  
  .register-link:hover {
    text-decoration: underline;
  }
  </style>