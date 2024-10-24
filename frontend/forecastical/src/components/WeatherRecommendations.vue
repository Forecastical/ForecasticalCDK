<template>
    <div class="weather-app">
      <div class="content">
        <div class="recommendations-container">
          <h2 class="title">Weather Recommendations for {{ currentLocation }}</h2>

            <!-- Add this new weather overview section -->
            <div class="weather-overview" v-if="weatherData">
            <div class="current-conditions">
                <div class="condition-item">
                <span class="label">Temperature:</span>
                <span class="value">{{ weatherData.current.temp_f }}°F</span>
                </div>
                <div class="condition-item">
                <span class="label">Conditions:</span>
                <span class="value">{{ weatherData.current.condition.text }}</span>
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
    export default {
    name: 'WeatherRecommendations',
    data() {
      return {
        showClothing: false,
        showTools: false,
        showActivities: false,
        currentLocation: "",
        weatherData: null,
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
        if (!this.weatherData) return this.recommendations.mild;
        
        const condition = this.weatherData.current.condition.text.toLowerCase();
        const temp = this.weatherData.current.temp_f;
        const windSpeed = this.weatherData.current.wind_mph;
        
        // Check for rain/storm conditions first
        if (condition.includes('rain') || condition.includes('storm') || condition.includes('drizzle')) {
          return this.recommendations.rainy;
        }
        
        // Check for high winds
        if (windSpeed > 20) {
          return this.recommendations.windy;
        }
        
        // Temperature-based recommendations
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
        try {
        const apiKey = process.env.VUE_APP_API_KEY;
        
        // Fetch location data
        const locationResponse = await fetch(`http://api.weatherapi.com/v1/ip.json?key=${apiKey}&q=auto:ip`);
        const locationData = await locationResponse.json();
        
        // Fetch current weather data
        const weatherResponse = await fetch(`https://api.weatherapi.com/v1/forecast.json?key=${apiKey}&q=${locationData.lat},${locationData.lon}&days=7&aqi=yes`);
        const weatherData = await weatherResponse.json();
        
        this.weatherData = weatherData;
        this.currentLocation = `${weatherData.location.name}, ${weatherData.location.region}`;
        } catch (error) {
        console.error('Error fetching weather data:', error);
        }
    },
    getRecommendationBasis() {
        if (!this.weatherData) return '';
        
        const condition = this.weatherData.current.condition.text.toLowerCase();
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
    },
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