<template>
  <div class="weather-app">
    <div class="content">
      <div class="left-column">
        <div class="current-weather">
          <h2>Current Weather & Forecast</h2>
          <p class="location">{{ currentLocation }}</p>
          <div class="weather-info">
            <img :src="currentWeatherIcon" alt="Weather icon" class="weather-icon" />
            <div class="temperature-condition">
              <p class="temperature">{{ temperature }}&deg;F</p>
              <p class="condition">{{ condition }}</p>
            </div>
          </div>
          <p class="forecast">Today's Forecast: {{ todayForecast }}</p>
        </div>
        <div class="weekly-forecast">
          <h2>Weekly Forecast</h2>
          <div class="forecast-grid">
            <div v-for="dayForecast in weeklyConditions" :key="dayForecast.day" class="day">
              <h4>{{ dayForecast.day }}</h4>
              <img :src="dayForecast.icon" alt="weather icon" class="weather-icon" />
              <p>
                {{ dayForecast.condition }}<br />
                {{ dayForecast.temperature }}&deg;F
              </p>
            </div>
          </div>
        </div>
        <div class="update-location">
          <button @click="fetchWeatherData">
            <span class="icon">↻</span>
            Update Weather
          </button>
        </div>
      </div>
      <div class="right-column">
        <div class="supplementary-conditions">
          <h2>Supplementary Conditions</h2>
          <p><strong>Air Quality:</strong> {{ air }}</p>
          <p><strong>UV Index:</strong> {{ uvIndex }}</p>
          <p><strong>Humidity:</strong> {{ humidity }}</p>
          <p><strong>Pressure:</strong> {{ pressure }}</p>
        </div>
        <div class="updated-user-forecast">
          <h2>Updated User Forecast</h2>
          <img src="/api/placeholder/300/200" alt="User forecast map placeholder" class="forecast-map" />
        </div>
      </div>
      <div class="innerdiv">
        <MapCard />
      </div>
    </div>
  </div>
</template>

<script>
import MapCard from './MapCard.vue'; 

export default {

  components: {
    MapCard,
  },

  name: "WeatherApp",
  data() {
    return {
      currentLocation: "",
      temperature: "",
      condition: "",
      currentWeatherIcon: "",
      air: "",
      uvIndex: "",
      humidity: "",
      pressure: "",
      todayForecast: "",
      weeklyConditions: [],
    };
  },
  methods: {
    async fetchWeatherData() {
      try {
        const apiKey = process.env.VUE_APP_API_KEY;
        
        // Fetch location data
        const locationResponse = await fetch(`http://api.weatherapi.com/v1/ip.json?key=${apiKey}&q=auto:ip`);
        const locationData = await locationResponse.json();
        
        // Fetch current weather data
        const weatherResponse = await fetch(`https://api.weatherapi.com/v1/forecast.json?key=${apiKey}&q=${locationData.lat},${locationData.lon}&days=7&aqi=yes`);
        const weatherData = await weatherResponse.json();
        
        // Update component data
        this.currentLocation = `${weatherData.location.name}, ${weatherData.location.region}`;
        this.temperature = Math.round(weatherData.current.temp_f);
        this.condition = weatherData.current.condition.text;
        this.currentWeatherIcon = `https:${weatherData.current.condition.icon}`;
        this.air = this.getAirQualityDescription(weatherData.current.air_quality["us-epa-index"]);
        this.uvIndex = weatherData.current.uv;
        this.humidity = `${weatherData.current.humidity}%`;
        this.pressure = `${weatherData.current.pressure_mb} hPa`;
        
        // Set today's forecast
        this.todayForecast = weatherData.forecast.forecastday[0].day.condition.text;
        
        // Set weekly forecast
        this.weeklyConditions = weatherData.forecast.forecastday.map(day => ({
          day: new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' }),
          condition: day.day.condition.text,
          temperature: Math.round(day.day.avgtemp_f),
          icon: `https:${day.day.condition.icon}`
        }));
      } catch (error) {
        console.error('Error fetching weather data:', error);
      }
    },
    getAirQualityDescription(index) {
      const descriptions = ["Good", "Moderate", "Unhealthy for Sensitive Groups", "Unhealthy", "Very Unhealthy", "Hazardous"];
      return descriptions[index - 1] || "Unknown";
    }
  },
  mounted() {
    this.fetchWeatherData();
  }
};
</script>

<style scoped>
.weather-app {
  font-family: Arial, sans-serif;
  color: white;
  background-color: #1e1e1e;
  padding: 0 20px 20px 20px; /* Add this line */
  border-radius: 10px;
  max-width: 1200px;
  margin: 0 auto;
}

.content {
  display: flex;
  gap: 20px;
}

.left-column {
  flex: 3;
}

.right-column {
  flex: 1;
}

.current-weather, .weekly-forecast, .supplementary-conditions, .updated-user-forecast {
  background-color: #34495e;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 5px;
}

.current-weather {
  text-align: center;
}

.current-weather .weather-info {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
}

.current-weather .weather-icon {
  width: 80px;
  height: 80px;
  margin-right: 20px;
}

.current-weather .temperature-condition {
  text-align: left;
}

.current-weather .temperature {
  font-size: 2.5em;
  margin: 0;
}

.current-weather .condition {
  font-size: 1.2em;
  color: #50e2e7;
  margin: 0;
}

.current-weather .forecast {
  margin-top: 15px;
  font-size: 1.1em;
}

.forecast-grid {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}

.forecast-grid .day {
  text-align: center;
  flex: 1;
  min-width: 100px;
  margin-bottom: 10px;
}

.forecast-grid .weather-icon {
  width: 50px;
  height: 50px;
}

.update-location button {
  background-color: #3498db;
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s;
}

.update-location button:hover {
  background-color: #2980b9;
}

.forecast-map {
  width: 100%;
  border-radius: 5px;
}

h2 {
  color: #50e2e7;
  margin-top: 0;
}

strong {
  color: #50e2e7;
}
</style>