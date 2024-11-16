import axios from 'axios';

const BASE_URL = 'https://api.open-meteo.com/v1';

export class WeatherService {
  constructor() {
    this.client = axios.create({
      baseURL: BASE_URL,
      timeout: 10000,
    });
  }

  /**
   * Get weather forecast for a specific location
   * @param {Object} params
   * @param {number} params.latitude - Location latitude
   * @param {number} params.longitude - Location longitude
   * @param {string} [params.timezone='auto'] - Location timezone
   * @param {number} [params.days=7] - Number of forecast days (max 16)
   * @returns {Promise<Object>} Weather forecast data
   */
  async getForecast({
    latitude,
    longitude,
    timezone = 'auto',
    days = 7
  }) {
    try {
      const response = await this.client.get('/forecast', {
        params: {
          latitude,
          longitude,
          timezone,
          forecast_days: days,
          hourly: [
            'temperature_2m',
            'relative_humidity_2m',
            'apparent_temperature',
            'precipitation_probability',
            'precipitation',
            'weather_code',
            'wind_speed_10m',
            'wind_direction_10m'
          ].join(','),
          daily: [
            'weather_code',
            'temperature_2m_max',
            'temperature_2m_min',
            'apparent_temperature_max',
            'apparent_temperature_min',
            'sunrise',
            'sunset',
            'precipitation_sum',
            'precipitation_probability_max',
            'wind_speed_10m_max'
          ].join(','),
        }
      });
      
      return response.data;
    } catch (error) {
      console.error('Error fetching weather forecast:', error);
      throw error;
    }
  }

  /**
   * Get current weather for a specific location
   * @param {Object} params
   * @param {number} params.latitude - Location latitude
   * @param {number} params.longitude - Location longitude
   * @param {string} [params.timezone='auto'] - Location timezone
   * @returns {Promise<Object>} Current weather data
   */
  async getCurrentWeather({
    latitude,
    longitude,
    timezone = 'auto'
  }) {
    try {
      const response = await this.client.get('/forecast', {
        params: {
          latitude,
          longitude,
          timezone,
          current: [
            'temperature_2m',
            'relative_humidity_2m',
            'apparent_temperature',
            'is_day',
            'precipitation',
            'rain',
            'weather_code',
            'wind_speed_10m',
            'wind_direction_10m'
          ].join(',')
        }
      });
      
      return response.data;
    } catch (error) {
      console.error('Error fetching current weather:', error);
      throw error;
    }
  }
}

// Create a singleton instance
export const weatherService = new WeatherService();

// Weather codes mapping
export const WEATHER_CODES = {
  0: 'Clear sky',
  1: 'Mainly clear',
  2: 'Partly cloudy',
  3: 'Overcast',
  45: 'Foggy',
  48: 'Depositing rime fog',
  51: 'Light drizzle',
  53: 'Moderate drizzle',
  55: 'Dense drizzle',
  56: 'Light freezing drizzle',
  57: 'Dense freezing drizzle',
  61: 'Slight rain',
  63: 'Moderate rain',
  65: 'Heavy rain',
  66: 'Light freezing rain',
  67: 'Heavy freezing rain',
  71: 'Slight snow fall',
  73: 'Moderate snow fall',
  75: 'Heavy snow fall',
  77: 'Snow grains',
  80: 'Slight rain showers',
  81: 'Moderate rain showers',
  82: 'Violent rain showers',
  85: 'Slight snow showers',
  86: 'Heavy snow showers',
  95: 'Thunderstorm',
  96: 'Thunderstorm with slight hail',
  99: 'Thunderstorm with heavy hail'
};