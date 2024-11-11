<template>
    <div class="api-test-container">
      <h1>Enhanced Weather API Test Component</h1>
      
      <!-- Location Search Test -->
      <div class="test-section">
        <h2>Location Search Test</h2>
        <div class="input-group">
          <div class="search-input">
            <label>Search Location:</label>
            <input type="text" v-model="searchQuery" placeholder="Enter city name..." />
            <button @click="searchLocation" class="btn" :disabled="loading.search">
              {{ loading.search ? 'Searching...' : 'Search' }}
            </button>
          </div>
        </div>
        <div v-if="error.search" class="error">
          Error: {{ error.search }}
        </div>
        <div v-if="results.search" class="results">
          <h3>Search Results:</h3>
          <div class="location-results">
            <div v-for="location in results.search" :key="location.id" 
                 class="location-item" @click="selectLocation(location)">
              <h4>{{ location.name }}</h4>
              <p>{{ location.admin1 }}, {{ location.country }}</p>
              <p class="coordinates">{{ location.latitude }}, {{ location.longitude }}</p>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Current Location Test -->
      <div class="test-section">
        <h2>Current Location</h2>
        <div class="input-group">
          <div>
            <label>Latitude:</label>
            <input type="number" v-model="latitude" step="0.01" />
          </div>
          <div>
            <label>Longitude:</label>
            <input type="number" v-model="longitude" step="0.01" />
          </div>
          <button @click="getLocation" class="btn">
            Get My Location
          </button>
        </div>
        <div v-if="results.reverseGeocode" class="results">
          <h3>Location Details:</h3>
          <pre>{{ JSON.stringify(results.reverseGeocode, null, 2) }}</pre>
        </div>
      </div>
  
      <!-- Complete Weather Data Test -->
      <div class="test-section">
        <h2>Complete Weather Data Test</h2>
        <button @click="fetchAllWeatherData" class="btn" :disabled="loading.all">
          {{ loading.all ? 'Loading...' : 'Fetch All Weather Data' }}
        </button>
        <div v-if="error.all" class="error">
          Error: {{ error.all }}
        </div>
        
        <div v-if="allWeatherData" class="results">
          <h3>Current Conditions:</h3>
          <ul>
            <li>Location: {{ allWeatherData.location }}</li>
            <li>Temperature: {{ allWeatherData.current.temperature }}°C</li>
            <li>Feels Like: {{ allWeatherData.current.apparentTemperature }}°C</li>
            <li>Weather: {{ allWeatherData.current.weatherDescription }}</li>
            <li>Humidity: {{ allWeatherData.current.humidity }}%</li>
            <li>Wind: {{ allWeatherData.current.windSpeed }} km/h</li>
            <li>Precipitation Probability: {{ allWeatherData.current.precipitationProbability }}%</li>
          </ul>
  
          <h3>Daily Forecast:</h3>
          <div class="forecast-summary">
            <div v-for="day in allWeatherData.daily" :key="day.date" class="forecast-day">
              <h4>{{ new Date(day.date).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' }) }}</h4>
              <ul>
                <li>Max: {{ day.tempMax }}°C</li>
                <li>Min: {{ day.tempMin }}°C</li>
                <li>Weather: {{ day.weatherDescription }}</li>
                <li>Precipitation: {{ day.precipitationProbability }}%</li>
                <li>Sunrise: {{ formatTime(day.sunrise) }}</li>
                <li>Sunset: {{ formatTime(day.sunset) }}</li>
              </ul>
            </div>
          </div>
  
          <h3>Raw API Responses:</h3>
          <div class="collapsible">
            <button @click="toggleRawData" class="btn">
              {{ showRawData ? 'Hide' : 'Show' }} Raw Data
            </button>
            <div v-if="showRawData" class="raw-data">
              <h4>Current Weather:</h4>
              <pre>{{ JSON.stringify(results.current, null, 2) }}</pre>
              <h4>Forecast:</h4>
              <pre>{{ JSON.stringify(results.forecast, null, 2) }}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { weatherService, WEATHER_CODES } from '@/services/weatherApi';
  import { geocodingService } from '@/services/geocodingApi';
  
  export default {
    name: 'WeatherApiTest',
    
    data() {
    return {

        latitude: 41.4995,  // Default to Cleveland
        longitude: -81.6954,
        searchQuery: '',
        showRawData: false,
        loading: {
        search: false,
        current: false,
        forecast: false,
        all: false
        },
        error: {
        search: null,
        current: null,
        forecast: null,
        all: null
        },
        results: {
        search: null,
        current: null,
        forecast: null,
        reverseGeocode: null
        },
        allWeatherData: null
        };
    },
  
    methods: {
        async searchLocation() {
            if (!this.searchQuery.trim()) return;
            
            this.loading.search = true;
            this.error.search = null;
            this.results.search = null;

            try {
                const results = await geocodingService.searchLocations(this.searchQuery);
                this.results.search = results;
                if (results.length === 0) {
                    this.error.search = 'No locations found';
                }
            } catch (error) {
            console.error('Error searching location:', error);
            this.error.search = 'Error searching location';
            } finally {
            this.loading.search = false;
            }
    },
  
      async selectLocation(location) {
        this.latitude = location.latitude;
        this.longitude = location.longitude;
        await this.fetchAllWeatherData();
      },
  
      async getLocation() {
        try {
          const position = await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject);
          });
          
          this.latitude = position.coords.latitude;
          this.longitude = position.coords.longitude;
          await this.reverseGeocode();
          await this.fetchAllWeatherData();
        } catch (error) {
          console.error('Error getting location:', error);
          alert('Could not get your location. Please enter coordinates manually.');
        }
      },
  
      async reverseGeocode() {
        try {
          const result = await geocodingService.reverseGeocode(this.latitude, this.longitude);
          this.results.reverseGeocode = result;
        } catch (error) {
          console.error('Error reverse geocoding:', error);
        }
      },
  
      async fetchAllWeatherData() {
      this.loading.all = true;
      this.error.all = null;
      this.allWeatherData = null;

      try {
        // Fetch weather data first
        const [current, forecast] = await Promise.all([
          weatherService.getCurrentWeather({ 
            latitude: this.latitude, 
            longitude: this.longitude 
          }),
          weatherService.getForecast({ 
            latitude: this.latitude, 
            longitude: this.longitude, 
            days: 7 
          })
        ]);

        // Then get location data
        const location = await geocodingService.reverseGeocode(
          this.latitude, 
          this.longitude
        );

        // Store raw responses
        this.results.current = current;
        this.results.forecast = forecast;
        this.results.reverseGeocode = location;

        // Process data into friendly format
        this.allWeatherData = {
          location: location.name ? 
            `${location.name}${location.admin1 ? `, ${location.admin1}` : ''}` : 
            `${this.latitude.toFixed(2)}°, ${this.longitude.toFixed(2)}°`,
          current: {
            temperature: current.current?.temperature_2m || 'N/A',
            apparentTemperature: current.current?.apparent_temperature || 'N/A',
            weatherDescription: current.current?.weather_code ? 
              WEATHER_CODES[current.current.weather_code] : 'Unknown',
            humidity: current.current?.relative_humidity_2m || 'N/A',
            windSpeed: current.current?.wind_speed_10m || 'N/A',
            precipitationProbability: current.current?.precipitation_probability || 0
          },
          daily: forecast.daily?.time.map((time, index) => ({
            date: time,
            tempMax: forecast.daily.temperature_2m_max[index],
            tempMin: forecast.daily.temperature_2m_min[index],
            weatherDescription: WEATHER_CODES[forecast.daily.weather_code[index]],
            precipitationProbability: forecast.daily.precipitation_probability_max[index],
            sunrise: forecast.daily.sunrise[index],
            sunset: forecast.daily.sunset[index]
          })) || []
        };
      } catch (error) {
        console.error('Error fetching weather data:', error);
        this.error.all = 'Error fetching weather data. Please try again.';
      } finally {
        this.loading.all = false;
      }
    },
  
      formatTime(isoString) {
        return new Date(isoString).toLocaleTimeString('en-US', {
          hour: 'numeric',
          minute: '2-digit'
        });
      },
  
      toggleRawData() {
        this.showRawData = !this.showRawData;
      }
    }
  };
  </script>
  
  
  <style scoped>
  .api-test-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    font-family: Avenir, Helvetica, Arial, sans-serif;
    color: #ffffff;
  }
  
  .test-section {
    background: #34495e;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 8px;
  }
  
  .input-group {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
    align-items: center;
  }
  
  .input-group div {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  input {
    padding: 8px;
    border: 1px solid #50e2e7;
    border-radius: 4px;
    width: 100px;
    background: #2c3e50;
    color: white;
  }
  
  .btn {
    padding: 8px 16px;
    background-color: #50e2e7;
    color: #1e1e1e;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
  }
  
  .btn:disabled {
    background-color: #2c3e50;
    cursor: not-allowed;
  }
  
  .btn:hover:not(:disabled) {
    background-color: #3fd1d6;
  }
  
  .error {
    color: #ff6b6b;
    margin: 10px 0;
    padding: 10px;
    background-color: rgba(255, 107, 107, 0.1);
    border-radius: 4px;
  }
  
  .results {
    margin-top: 20px;
  }
  
  pre {
    background-color: #2c3e50;
    padding: 15px;
    border-radius: 4px;
    overflow-x: auto;
    font-size: 14px;
    color: #50e2e7;
  }
  
  .forecast-summary {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-top: 20px;
  }
  
  .forecast-day {
    background-color: #2c3e50;
    padding: 15px;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .forecast-day h4 {
    margin: 0 0 10px 0;
    color: #50e2e7;
  }
  
  .forecast-day ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .forecast-day li {
    margin-bottom: 5px;
    font-size: 14px;
    color: #ffffff;
  }
  
  h1, h2, h3 {
    color: #50e2e7;
  }
  .search-input {
    display: flex;
    gap: 10px;
    flex: 1;
  }
  
  .search-input input {
    flex: 1;
    min-width: 300px;
  }
  
  .location-results {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 15px;
    margin-top: 15px;
  }
  
  .location-item {
    background-color: #2c3e50;
    padding: 15px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .location-item:hover {
    background-color: #3c526a;
  }
  
  .location-item h4 {
    margin: 0 0 5px 0;
    color: #50e2e7;
  }
  
  .location-item p {
    margin: 5px 0;
    font-size: 14px;
  }
  
  .coordinates {
    color: #8795a1;
    font-size: 12px;
  }
  
  .collapsible .btn {
    margin: 10px 0;
  }
  
  .raw-data {
    margin-top: 15px;
  }
  
  .raw-data h4 {
    color: #50e2e7;
    margin: 15px 0 10px 0;
  }
  </style>