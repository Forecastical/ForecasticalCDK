// src/services/weatherFeedService.js
import { authService } from './authService';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

class WeatherFeedService {
  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      timeout: 5000,
      headers: {
        'Accept': 'application/json'
      },
      withCredentials: true
    });
  }

  async uploadImage(file, caption) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('caption', caption);

      const currentUser = authService.getCurrentUser();
      if (!currentUser) {
        throw new Error('User not authenticated');
      }

      const auth = {
        username: currentUser.username,
        password: currentUser.password
      };

      formData.append('auth', JSON.stringify(auth));

      const response = await this.client.post('/upload_image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      return response.data;
    } catch (error) {
      console.error('Error uploading image:', error);
      throw error;
    }
  }

  async getFeedImages() {
    try {
      const currentUser = authService.getCurrentUser();
      if (!currentUser) {
        throw new Error('User not authenticated');
      }

      // Pass auth data as query parameters instead of body
      const response = await this.client.get('/feed_images', {
        params: {
          username: currentUser.username,
          password: currentUser.password
        }
      });

      return response.data;
    } catch (error) {
      console.error('Error fetching feed images:', error);
      throw error;
    }
  }
  async deleteImage(imageId) {
    try {
      const currentUser = authService.getCurrentUser();
      if (!currentUser) {
        throw new Error('User not authenticated');
      }

      const response = await this.client.delete(`/feed_images/${imageId}`, {
        params: {
          username: currentUser.username,
          password: currentUser.password
        }
      });

      return response.data;
    } catch (error) {
      console.error('Error deleting image:', error);
      throw error;
    }
  }

  getAuthHeader() {
    const user = authService.getCurrentUser();
    if (user) {
      return { Authorization: `Basic ${btoa(`${user.username}:${user.password}`)}` };
    }
    return {};
  }
}

export const weatherFeedService = new WeatherFeedService();
