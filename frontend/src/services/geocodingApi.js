import axios from 'axios';

const GEOCODING_URL = 'https://geocoding-api.open-meteo.com/v1';

export class GeocodingService {
  constructor() {
    this.geocodingClient = axios.create({
      baseURL: GEOCODING_URL,
      timeout: 5000,
      headers: {
        'Accept': 'application/json'
      }
    });
  }

  /**
   * Search for locations by name
   * @param {string} query - City name or address
   * @returns {Promise<Array>} Array of location matches
   */
  async searchLocations(query) {
    try {
      const response = await this.geocodingClient.get('/search', {
        params: {
          name: query,
          count: 10,
          language: 'en',
          format: 'json'
        }
      });
      
      return response.data.results || [];
    } catch (error) {
      console.error('Error searching locations:', error);
      return [];
    }
  }

  /**
   * Get location name from coordinates
   * @param {number} latitude 
   * @param {number} longitude 
   * @returns {Promise<Object>} Location information
   */
  async reverseGeocode(latitude, longitude) {
    try {
      // Add validation for coordinates
      if (latitude === undefined || longitude === undefined) {
        throw new Error('Invalid coordinates provided');
      }

      // First try to search for nearby locations
      const response = await this.geocodingClient.get('/search', {
        params: {
          name: '',
          latitude: parseFloat(latitude),
          longitude: parseFloat(longitude),
          radius: 10000,
          count: 1,
          language: 'en',
          format: 'json'
        }
      });
      
      if (response.data.results?.[0]) {
        return response.data.results[0];
      }

      // Fallback to coordinate display if no location found
      return {
        name: `${parseFloat(latitude).toFixed(2)}°`,
        admin1: `${parseFloat(longitude).toFixed(2)}°`,
        country: 'Unknown Location'
      };
    } catch (error) {
      console.error('Error reverse geocoding:', error);
      // Return a default location object instead of throwing
      return {
        name: 'Unknown Location',
        admin1: '',
        country: ''
      };
    }
  }
}

export const geocodingService = new GeocodingService();
