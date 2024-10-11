<template>
  <div class="weather-app">
    <header>
      <h1>Forecastical</h1>
      <router-link to="/profile">Go to Profile</router-link>
    </header>
    <div class="content">
      <div class="left-column">
        <div class="current-weather">
          <p>Current Location: {{ currentLocation }}</p>
          <p>{{ temperature }} degrees; {{ condition }}</p>
          <span class="weather-icon">☁️</span>
        </div>
        <div class="today-forecast">
          <h2>Today's Forecast</h2>
          <div></div>
          <!-- TODO: Add today's forecast details here and connect to NWS-->
        </div>
        <div class="weekly-forecast">
          <h2>Weekly Forecast</h2>
          <div class="forecast-grid">
            <div
              v-for="dayForecast in weeklyConditions"
              :key="dayForecast.day"
              class="day"
            >
              <h4>{{ dayForecast.day }}</h4>
              <img
                :src="getWeatherIcon(dayForecast.condition)"
                alt="weather icon"
                class="weather-icon"
              />
              <p>
                {{ dayForecast.condition }}<br />
                {{ dayForecast.temperature }}&deg;
              </p>
            </div>
          </div>
        </div>
        <div class="update-location">
          <button @click="updateLocation">
            <span class="icon">↻</span>
            Update Location
          </button>
        </div>
      </div>
      <!-- New button to fetch weather data -->
      <div class="fetch-weather-data">
        <button @click="fetchWeatherData">
          Fetch Weather Data
        </button>
      </div>
      <div class="right-column">
        <div class="supplementary-conditions">
          <h2>Supplementary Conditions</h2>
          <p>Air: {{ air }}</p>
          <p>UV Index: {{ uvIndex }}</p>
          <p>Humidity: {{ humidity }}</p>
          <p>Pressure: {{ pressure }}</p>
        </div>
        <div class="updated-user-forecast">
          <h2>Updated User Forecast</h2>
          <!-- TODO: Add user forecast map or details here once we get ML stuff going-->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "WeatherApp",
  data() {
    return {
      currentLocation: "Cleveland, OH",
      temperature: 42,
      condition: "Partly cloudy",
      air: "23",
      uvIndex: "9",
      humidity: "78%",
      pressure: "1,014 hPa",
      weatherIcons: {
        sunny: require("../assets/sunny.png"),
        rainy: require("../assets/rainy.png"),
        partly_cloudy: require("../assets/partly_cloudy.png"),
      },
      weeklyConditions: [
        { day: "Sunday", condition: "sunny", temperature: "79" },
        { day: "Monday", condition: "partly cloudy", temperature: "73" },
        { day: "Tuesday", condition: "rainy", temperature: "60" },
        { day: "Wednesday", condition: "partly cloudy", temperature: "67" },
        { day: "Thursday", condition: "sunny", temperature: "75" },
        { day: "Friday", condition: "partly cloudy", temperature: "73" },
        { day: "Saturday", condition: "rainy", temperature: "71" },
      ],
    };
  },
  methods: {
    updateLocation() {
      // TODO: Implement location update logic here
      console.log("Updating location...");
    },
    getWeatherIcon(condition) {
      // Map of the weather condition to the weather icon
      const conditionMapping = {
        "partly cloudy": "partly_cloudy",
        cloudy: "cloudy",
        sunny: "sunny",
        rainy: "rainy",
      };
      const mappedCondition =
        conditionMapping[condition.toLowerCase()] || "default";
      return this.weatherIcons[mappedCondition];
    },
    fetchWeatherData() {
      console.log("HELLO");
      const apiKey = process.env.VUE_APP_API_KEY;
      const location = "Cleveland";

      console.log("API Key:", apiKey); // This will help us debug


      fetch(`https://api.weatherapi.com/v1/current.json?key=${apiKey}&q=${location}`)
        .then(response => {
          if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
          }
          return response.json();
        })
        .then(data => {
          // Log the data to the console to see if the response is working
          console.log('API response:', data);

          // Parse and use the data
          this.currentLocation = data.location.name + ", " + data.location.region;
          this.temperature = data.current.temp_f; // For Fahrenheit
          this.condition = data.current.condition.text;
          this.air = data.current.air_quality?.us_epa_index || "N/A";
          this.uvIndex = data.current.uv;
          this.humidity = data.current.humidity + "%";
          this.pressure = data.current.pressure_mb + " hPa";
        })
        .catch(error => {
          // Log the error if something goes wrong
          console.error('Error fetching weather data:', error);
      });
    }
  },
  computed: {
    weatherIcon() {
      // Map of the weather conditions to their corresponding icons
      const conditionMapping = {
        "Partly cloudy": "partly_cloudy",
        cloudy: "partly_cloudy",
        sunny: "Sunny",
        rainy: "Rainy",
      };

      const mappedCondition =
        conditionMapping[this.condition] || this.condition;
      return (
        this.weatherIcons[mappedCondition] ||
        require("../assets/partly_cloudy.png")
      );
    },
  },
};
</script>

<style scoped>
.weather-app {
  font-family: Arial, sans-serif;
  color: white;
  background-color: #1e1e1e;
  padding: 20px;
  border-radius: 10px;
}

header {
  background-color: #50e2e7;
  padding: 10px;
  text-align: center;
  border-radius: 5px;
}

.content {
  display: flex;
  margin-top: 20px;
}

.left-column {
  flex: 3;
  margin-right: 20px;
}

.right-column {
  flex: 1;
}

.update-location,
.current-weather,
.today-forecast,
.weekly-forecast,
.supplementary-conditions,
.updated-user-forecast {
  background-color: #34495e;
  padding: 15px;
  margin-bottom: 20px;
  border-radius: 5px;
}

.update-location button {
  background-color: #3498db;
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.weather-icon {
  font-size: 2em;
}

h2 {
  margin-top: 0;
}

.weekly-forecast .forecast-grid {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap; /* wrap for small screen size */
}

.weekly-forecast .day {
  flex: 1 1 calc(100% / 7);
  max-width: 100px; 
  text-align: center;
}

.weekly-forecast img {
  width: 50px;
  height: 50px;
}
</style>
