// src/services/authService.js
import axios from 'axios';

const API_URL = 'http://localhost:8000';

class AuthService {
  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      timeout: 5000,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      withCredentials: true
    });
  }

  async login(username, password) {
    try {
      const response = await this.client.post('/user/validate', {
        username,
        password
      });
      
      if (response.data) {
        // Make sure user object includes location data
        const userData = {
          username,
          password,
          home_lat: 41.5034, // Default to Cleveland, OH if not provided
          home_lon: -81.6964, // These should come from your backend
          ...response.data
        };
        localStorage.setItem('user', JSON.stringify(userData));
        return userData;
      }
      return null;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  async register(userData) {
    try {
      const response = await this.client.post('/user', {
        username: userData.username,
        password: userData.password,
        user_fname: userData.firstName,
        user_lname: userData.lastName,
        user_age: userData.age,
        home_lat: userData.latitude,
        home_lon: userData.longitude,
        use_celsius: userData.useCelsius,
        user_alerts: userData.enableAlerts
      });
      return response.data;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  }

  async updateUser(userData) {
    try {
      const response = await this.client.patch('/user', userData, {
        headers: this.getAuthHeader()
      });
      return response.data;
    } catch (error) {
      console.error('Update user error:', error);
      throw error;
    }
  }

  logout() {
    localStorage.removeItem('user');
  }

  getCurrentUser() {
    return JSON.parse(localStorage.getItem('user'));
  }

  getAuthHeader() {
    const user = this.getCurrentUser();
    if (user) {
      return { Authorization: `Basic ${btoa(`${user.username}:${user.password}`)}` };
    }
    return {};
  }
}

export const authService = new AuthService();
