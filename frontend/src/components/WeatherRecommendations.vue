<template>
    <div class="weather-app">
      <div class="content">
        <div class="recommendations-container">

          <h2 class="title">{{ currentLocation }} Weather Recommendations </h2>

            <div v-if="loading" class="loading">
              Loading weather data...
            </div>

            <div v-else-if="error" class="error">
              {{ error }}
            </div>

            <div class="weather-overview" v-if="weatherData && weatherData.current">
            <div class="current-conditions">
              <div class="condition-item">
                <span class="label">Temperature:</span>
                <span class="value">{{ weatherData.current.temp_f }}°F</span>
              </div>
              <div class="condition-item">
                <span class="label">Conditions:</span>
                <span class="value">{{ weatherData.current?.condition?.text || 'N/A' }}</span>
              </div>
              <div class="condition-item">
                <span class="label">Wind:</span>
                <span class="value">{{ weatherData.current.wind_mph }} mph</span>
              </div>
            </div>

            <p class="recommendation-basis">
                Recommendations based on {{ getRecommendationBasis() }}
            </p>
            </div>
          
          <div class="recommendation-card clothing" @click="toggleClothing">
            <div class="card-content">
              <span class="card-text">Click for clothing suggestions!</span>
              <span class="card-icon">👕</span>
            </div>
            <div class="recommendations-list" v-if="showClothing">
              <ul>
                <li v-for="(item, index) in currentRecommendations.clothing" :key="index">
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>
  
          <div class="recommendation-card tools" @click="toggleTools">
            <div class="card-content">
              <span class="card-text">Click for tool suggestions!</span>
              <span class="card-icon">🔧</span>
            </div>
            <div class="recommendations-list" v-if="showTools">
              <ul>
                <li v-for="(item, index) in currentRecommendations.tools" :key="index">
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>
  
          <div class="recommendation-card activities" @click="toggleActivities">
            <div class="card-content">
              <span class="card-text">Click for activity suggestions!</span>
              <span class="card-icon">🎾</span>
            </div>
            <div class="recommendations-list" v-if="showActivities">
              <ul>
                <li v-for="(item, index) in currentRecommendations.activities" :key="index">
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>

        </div>
      </div>
    </div>

  </template>
  
<script>
    import { useAuthStore } from '@/store/auth';
    import { weatherService } from '@/services/weatherApi';
    import { geocodingService } from '@/services/geocodingApi';

    const WEATHER_CONDITIONS = {
      0: 'clear sky',
      1: 'mainly clear',
      2: 'partly cloudy',
      3: 'overcast',
      45: 'foggy',
      48: 'depositing rime fog',
      51: 'light drizzle',
      53: 'moderate drizzle',
      55: 'dense drizzle',
      56: 'light freezing drizzle',
      57: 'dense freezing drizzle',
      61: 'slight rain',
      63: 'moderate rain',
      65: 'heavy rain',
      66: 'light freezing rain',
      67: 'heavy freezing rain',
      71: 'slight snow',
      73: 'moderate snow',
      75: 'heavy snow',
      77: 'snow grains',
      80: 'slight rain showers',
      81: 'moderate rain showers',
      82: 'violent rain showers',
      85: 'slight snow showers',
      86: 'heavy snow showers',
      95: 'thunderstorm',
      96: 'thunderstorm with slight hail',
      99: 'thunderstorm with heavy hail'
    };

    export default {
    name: 'WeatherRecommendations',
    data() {
      return {
        showClothing: false,
        showTools: false,
        showActivities: false,
        currentLocation: "",
        weatherData: null,
        error: null,
        loading: false,
        recommendations: {
          cold: {
            clothing: [
              'Heavy winter coat',
              'Thermal layers',
              'Gloves and scarf',
              'Warm boots'
            ],
            tools: [
              'Ice scraper',
              'Snow shovel',
              'Hand warmers',
              'Emergency blanket'
            ],
            activities: [
              'Indoor exercises',
              'Ice skating',
              'Museums visits',
              'Indoor crafts'
            ]
          },
          mild: {
            clothing: [
              'Light jacket or sweater',
              'Long sleeve shirt',
              'Comfortable pants',
              'Closed-toe shoes'
            ],
            tools: [
              'Umbrella',
              'Light jacket',
              'Water bottle',
              'Portable chair'
            ],
            activities: [
              'Walking or hiking',
              'Park visits',
              'Photography',
              'Outdoor dining'
            ]
          },
          warm: {
            clothing: [
              'Light, breathable clothing',
              'Short sleeves',
              'Sun hat',
              'Sunglasses'
            ],
            tools: [
              'Sunscreen',
              'Water bottle',
              'Portable fan',
              'Sun umbrella'
            ],
            activities: [
              'Beach visit',
              'Swimming',
              'Outdoor sports',
              'Gardening'
            ]
          },
          rainy: {
            clothing: [
              'Rain jacket',
              'Waterproof boots',
              'Quick-dry clothing',
              'Rain hat'
            ],
            tools: [
              'Sturdy umbrella',
              'Rain boots',
              'Waterproof bag',
              'Towel'
            ],
            activities: [
              'Indoor reading',
              'Movie watching',
              'Indoor games',
              'Museum visits'
            ]
          },
          windy: {
            clothing: [
              'Windbreaker',
              'Secured hat',
              'Protective eyewear',
              'Layer clothing'
            ],
            tools: [
              'Wind resistant umbrella',
              'Protective eyewear',
              'Secure bags',
              'Extra hair ties'
            ],
            activities: [
              'Kite flying',
              'Indoor activities',
              'Sheltered walks',
              'Photography'
            ]
          }
        }
      }
    },
    computed: {
      currentRecommendations() {
        if (!this.weatherData?.current) return this.recommendations.mild;
        
        const condition = this.weatherData.current.condition.text;
        const temp = this.weatherData.current.temp_f;
        const windSpeed = this.weatherData.current.wind_mph;
        
        if (condition.includes('rain') || condition.includes('storm') || condition.includes('drizzle')) {
          return this.recommendations.rainy;
        }
        
        if (windSpeed > 20) {
          return this.recommendations.windy;
        }
        
        if (temp < 45) {
          return this.recommendations.cold;
        } else if (temp > 75) {
          return this.recommendations.warm;
        } else {
          return this.recommendations.mild;
        }
      }
    },

    methods: {
    getWeatherDescription(code) {
      return WEATHER_CONDITIONS[code] || 'unknown';
    },
    toggleClothing() {
        this.showClothing = !this.showClothing;
    },
    toggleTools() {
        this.showTools = !this.showTools;
    },
    toggleActivities() {
        this.showActivities = !this.showActivities;
    },
    async fetchWeatherData() {
      this.loading = true;
      this.error = null;

      try {
        const auth = useAuthStore();
        const user = auth.user;

        if (!user) {
          throw new Error('User not authenticated');
        }

        // Validate coordinates
        if (!user.home_lat || !user.home_lon) {
          throw new Error('User location not set');
        }

        // Get current weather using weatherService
        const current = await weatherService.getCurrentWeather({
          latitude: user.home_lat,
          longitude: user.home_lon
        });

        // Get location name
        const location = await geocodingService.reverseGeocode(
          user.home_lat,
          user.home_lon
        );

        // Format the data to match your component's expectations
        this.weatherData = {
          current: {
            temp_f: (current.current.temperature_2m * 9/5) + 32,
            condition: {
              code: current.current.weather_code,
              text: this.getWeatherDescription(current.current.weather_code)
            },
            wind_mph: current.current.wind_speed_10m * 0.621371
          },
          location: {
            name: location.name || 'Unknown Location',
            region: location.admin1 || ''
          }
        };

        this.currentLocation = location.name && location.admin1 
          ? `${location.name}, ${location.admin1}`
          : 'Location Unavailable';

      } catch (error) {
        console.error('Error fetching weather data:', error);
        this.error = error.message || 'Failed to load weather data';
        this.weatherData = null;
        // Set a default location name when there's an error
        this.currentLocation = 'Location Unavailable';
      } finally {
        this.loading = false;
      }
    },
    getRecommendationBasis() {
      if (!this.weatherData?.current?.condition?.text) return '';
      
      const condition = this.weatherData.current.condition.text;
      const temp = this.weatherData.current.temp_f;
      const windSpeed = this.weatherData.current.wind_mph;
      
      if (condition.includes('rain') || condition.includes('storm') || condition.includes('drizzle')) {
        return 'rainy conditions';
      }
      
      if (windSpeed > 20) {
        return 'windy conditions';
      }
      
      if (temp < 45) {
        return 'cold temperatures';
      } else if (temp > 75) {
        return 'warm temperatures';
      } else {
        return 'mild conditions';
      }
    }
  },
    mounted() {
      this.fetchWeatherData();
    }
  }
</script>
  
  
<style scoped>
  .weather-app {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px 20px 20px;
  }
  
  .title {
    color: #50e2e7;
    font-size: 1.8em;
    margin-bottom: 30px;
  }
  
  .recommendations-container {
    width: 100%;
  }
  
  .recommendation-card {
    background-color: #34495e;
    border-radius: 10px;
    margin-bottom: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .recommendation-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .card-content {
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .card-text {
    font-size: 1.2em;
    color: white;
  }
  
  .card-icon {
    font-size: 1.5em;
  }
  
  .recommendations-list {
    padding: 0 20px 20px 20px;
    border-top: 1px solid #405468;
  }
  
  .recommendations-list ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .recommendations-list li {
    padding: 10px 0;
    color: #bdc3c7;
  }
  
  .clothing {
    background-color: rgba(52, 152, 219, 0.1);
  }
  
  .tools {
    background-color: rgba(241, 196, 15, 0.1);
  }
  
  .activities {
    background-color: rgba(231, 76, 60, 0.1);
  }
  
  @media (max-width: 768px) {
    .recommendation-card {
      margin: 10px 0;
    }
    
    .card-content {
      flex-direction: column;
      text-align: center;
      gap: 10px;
    }
  }

  .weather-overview {
    background-color: #34495e;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 30px;
    }

    .current-conditions {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 20px;
    margin-bottom: 15px;
    }

    .condition-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 120px;
    }

    .label {
    color: #50e2e7;
    font-size: 0.9em;
    margin-bottom: 5px;
    }

    .value {
    color: white;
    font-size: 1.2em;
    font-weight: bold;
    }

    .recommendation-basis {
    color: #bdc3c7;
    text-align: center;
    margin: 0;
    padding-top: 15px;
    border-top: 1px solid #405468;
    }

    @media (max-width: 768px) {
    .current-conditions {
        flex-direction: column;
        align-items: center;
        gap: 15px;
    }
    
    .condition-item {
        width: 100%;
        flex-direction: row;
        justify-content: space-between;
        gap: 10px;
    }
    }
</style>
