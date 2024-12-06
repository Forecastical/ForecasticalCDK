// src/services/weatherFeedService.js
import { authService } from './authService';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

class WeatherFeedService {
  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      timeout: 10000, // Increased timeout for image processing
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

      // After successful upload, immediately tag the image
      if (response.data && response.data.image_path) {
        try {
          const tagResult = await this.tagImage(response.data.image_path);
          return { ...response.data, weatherPrediction: tagResult.prediction };
        } catch (tagError) {
          console.warn('Image uploaded but tagging failed:', tagError);
          return response.data;
        }
      }

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

  async deletePost(imageId) {
    try {
      const currentUser = authService.getCurrentUser();
      if (!currentUser) {
        throw new Error('User not authenticated');
      }

      const response = await this.client.delete(`/post/${imageId}`, {
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

  async tagLatestImage(imageUrl) {
    try {
      const currentUser = authService.getCurrentUser();
      if (!currentUser) {
        throw new Error('User not authenticated');
      }

      // Convert URL to Blob
      const response = await fetch(`${this.client.defaults.baseURL}${imageUrl}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch image: ${response.statusText}`);
      }
      const blob = await response.blob();
      
      // Create form data
      const formData = new FormData();
      formData.append('username', currentUser.username);
      formData.append('password', currentUser.password);
      formData.append('file', blob, 'image.jpg');

      // Create a new axios instance with a longer timeout just for this request
      const tagClient = axios.create({
        baseURL: API_URL,
        timeout: 60000,  // 60 second timeout for ML processing
        headers: {
          'Accept': 'application/json'
        },
        withCredentials: true
      });

      const tagResponse = await tagClient.post('/tag_image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      return tagResponse.data;
    } catch (error) {
      console.error('Error tagging image:', error);
      throw error;
    }
  }

  // Helper method to get auth header if needed
  getAuthHeader() {
    const user = authService.getCurrentUser();
    if (user) {
      return { Authorization: `Basic ${btoa(`${user.username}:${user.password}`)}` };
    }
    return {};
  }
}

export const weatherFeedService = new WeatherFeedService();