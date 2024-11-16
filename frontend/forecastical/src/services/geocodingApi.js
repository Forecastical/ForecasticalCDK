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
   * Get location name from coordinates (reverse geocoding)
   * @param {number} latitude 
   * @param {number} longitude 
   * @returns {Promise<Object>} Location information
   */
  async reverseGeocode(latitude, longitude) {
    try {
      // First try to search for nearby locations
      const response = await this.geocodingClient.get('/search', {
        params: {
          name: '', // Empty name to search all locations
          latitude: latitude,
          longitude: longitude,
          radius: 10000, // 10km radius
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
        name: `${latitude.toFixed(2)}°, ${longitude.toFixed(2)}°`,
        admin1: 'Unknown Location',
        country: ''
      };
    } catch (error) {
      console.error('Error reverse geocoding:', error);
      return {
        name: `${latitude.toFixed(2)}°, ${longitude.toFixed(2)}°`,
        admin1: 'Unknown Location',
        country: ''
      };
    }
  }
}

export const geocodingService = new GeocodingService();