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

    getCurrentUser() {
        const userStr = localStorage.getItem('user');
        if (!userStr) return null;
        try {
            return JSON.parse(userStr);
        } catch (e) {
            console.error('Error parsing user data:', e);
            return null;
        }
    }


    async updateUser(userData) {
        try {
          const currentUser = this.getCurrentUser();
          if (!currentUser) {
            throw new Error('No authenticated user found');
          }
      
          // Separate auth and user_data as expected by the backend
          const requestBody = {
            auth: {
              username: currentUser.username,
              password: currentUser.password
            },
            user_data: userData  // This contains all the update fields
          };
      
          console.log('Sending request body:', requestBody);
      
          const response = await this.client.patch('/user', requestBody);
          
          if (response.data && response.data.user) {
            const updatedUserData = {
              ...currentUser,
              ...response.data.user,
              // Ensure user_age is properly mapped
              user_age: response.data.user.user_age
            };
            localStorage.setItem('user', JSON.stringify(updatedUserData));
            return updatedUserData;
          }
      
          return response.data;
        } catch (error) {
          console.error('Update user error:', error);
          if (error.response?.data?.detail) {
            const detail = error.response.data.detail;
            if (Array.isArray(detail)) {
              throw new Error(detail.map(err => err.msg).join('. '));
            } else {
              throw new Error(detail);
            }
          }
          throw new Error(error.message || 'Failed to update user');
        }
      }
}

const authService = new AuthService();
export { authService };