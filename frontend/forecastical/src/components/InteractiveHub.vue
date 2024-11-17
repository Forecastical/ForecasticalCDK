<template>
  <div class="weather-app">
    <div class="content">
      <div class="left-column">
        <div class="current-weather">
          <h2>Fact of the Day: {{ formattedDate }}</h2>
          <h4>{{ fact }}</h4>
          <p class="loc">{{ currentLocation }}</p>
        </div>
        <div class="current-weather">
          <div class="header-row">
            <h2>Today's Weather in:</h2>
            <h4>{{ currentLocation }}</h4>
          </div>
          <div class="weather-info">
            <WeatherIcon :code="weatherCode" class="weather-icon" />
            <div class="temperature-condition">
              <p class="temperature">{{ temperature }}&deg;C</p>
              <p class="condition">{{ condition }}</p>
            </div>
          </div>
          <p class="forecast">Today's Forecast: {{ todayForecast }}</p>
        </div>

        <div class="update-location">
          <button @click="fetchWeatherData" class="update-btn">
            <span class="icon">↻</span>
            Update Weather
          </button>
        </div>
      </div>

      <div class="right-column">
        <div class="supplementary-conditions">
          <h2>Current Conditions</h2>
          <p><strong>Feels Like:</strong> {{ feelsLike }}&deg;C</p>
          <p><strong>Humidity:</strong> {{ humidity }}</p>
          <p><strong>Wind Speed:</strong> {{ windSpeed }}</p>
          <p><strong>Pressure:</strong> {{ pressure }}</p>
          <p><strong>Precipitation:</strong> {{ precipitation }}%</p>
        </div>

        <div class="sun-times" v-if="sunTimes">
          <h2>Sun Times</h2>
          <p><strong>Sunrise:</strong> {{ formatTime(sunTimes.sunrise) }}</p>
          <p><strong>Sunset:</strong> {{ formatTime(sunTimes.sunset) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import WeatherIcon from "./WeatherIcon.vue";
import { weatherService, WEATHER_CODES } from "@/services/weatherApi";
import { geocodingService } from "@/services/geocodingApi";

export default {
  name: "InteractiveHub",

  components: {
    WeatherIcon,
  },

  data() {
    return {
      latitude: null,
      longitude: null,
      currentLocation: "Loading...",
      city: "Unknown city",
      state: "Unknown state",
      country: "Unknown country",
      temperature: "---",
      weatherCode: 0,
      condition: "---",
      feelsLike: "---",
      humidity: "---",
      windSpeed: "---",
      pressure: "---",
      precipitation: "---",
      todayForecast: "---",
      weeklyConditions: [],
      sunTimes: null,
      loading: false,
      error: null,
      fact: null,
      formattedDate: "",
    };
  },

  methods: {
    async fetchDataFromJson() {
      try {
        // Fetch JSON data from public folder
        const response = await fetch("/weather_facts.json");
        if (!response.ok) throw new Error("Failed to fetch JSON file");

        const data = await response.json();

        // Get today's date in the format YYYY-MM-DD
        // const today = new Date().toISOString().split("T")[0].split("-");
        // const formattedDate = today[1] + "/" + today[2];
        const today = new Date();
        const formattedDate = [
          String(today.getMonth() + 1).padStart(2, "0"), // Month
          String(today.getDate()).padStart(2, "0"), // Day
        ].join("/");
        this.formattedDate = formattedDate;

        console.log(formattedDate);

        // const today = new Date();
        // const formattedDate = `${String(today.getMonth() + 1).padStart(
        //   2,
        //   "0"
        // )}/${String(today.getDate()).padStart(2, "0")}`;
        // console.log("Formatted Date:", formattedDate);

        // Find the entry for today's date
        const todayRow = data.find(
          (row) => row["Current date"] === formattedDate
        );
        console.log(todayRow);

        if (todayRow) {
          // Set the fact
          this.fact = todayRow.Fact;
          console.log(this.fact);

          // Fetch coordinates for the location
          console.log(todayRow.Location);

          const locationData = todayRow.Location.split(", ");
          if (locationData) {
            this.latitude = parseFloat(locationData[0]);
            this.longitude = parseFloat(locationData[1]);
            // this.latitude = locationData[0];
            // this.longitude = locationData[1];

            // Fetch weather for this location
            await this.fetchWeatherData();
            await this.fetchCityName();
          }
        } else {
          this.fact = "No data available for today.";
        }
      } catch (error) {
        console.error("Error fetching data:", error);
        this.fact = "Could not load fact.";
      }
    },

    async fetchWeatherData() {
      try {
        this.loading = true;
        this.error = null;

        if (!this.latitude || !this.longitude) {
          const position = await this.getUserLocation();
          this.latitude = position.coords.latitude;
          this.longitude = position.coords.longitude;
        }

        // Fetch all data in parallel
        const [locationData, current, forecast] = await Promise.all([
          geocodingService.reverseGeocode(this.latitude, this.longitude),
          weatherService.getCurrentWeather({
            latitude: this.latitude,
            longitude: this.longitude,
          }),
          weatherService.getForecast({
            latitude: this.latitude,
            longitude: this.longitude,
            days: 7,
          }),
        ]);

        // Update location
        this.currentLocation =
          locationData.name && locationData.admin1
            ? `${locationData.name}, ${locationData.admin1}`
            : `${this.latitude.toFixed(2)}°, ${this.longitude.toFixed(2)}°`;

        // Update current weather
        this.temperature = Math.round(current.current.temperature_2m);
        this.weatherCode = current.current.weather_code;
        this.condition = WEATHER_CODES[this.weatherCode];
        this.feelsLike = Math.round(current.current.apparent_temperature);
        this.humidity = `${current.current.relative_humidity_2m}%`;
        this.windSpeed = `${current.current.wind_speed_10m} km/h`;
        this.pressure = `${current.current.surface_pressure} hPa`;
        this.precipitation = forecast.daily.precipitation_probability_max[0];

        // Update forecast
        this.todayForecast = WEATHER_CODES[forecast.daily.weather_code[0]];

        // Update weekly forecast
        this.weeklyConditions = forecast.daily.time.map((time, index) => ({
          day: new Date(time).toLocaleDateString("en-US", { weekday: "short" }),
          weatherCode: forecast.daily.weather_code[index],
          condition: WEATHER_CODES[forecast.daily.weather_code[index]],
          maxTemp: Math.round(forecast.daily.temperature_2m_max[index]),
          minTemp: Math.round(forecast.daily.temperature_2m_min[index]),
        }));

        // Update sun times
        this.sunTimes = {
          sunrise: forecast.daily.sunrise[0],
          sunset: forecast.daily.sunset[0],
        };
      } catch (error) {
        console.error("Error fetching weather data:", error);
        this.error = "Failed to fetch weather data";
      } finally {
        this.loading = false;
      }
    },

    async fetchCityName() {
      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/reverse?lat=${this.latitude}&lon=${this.longitude}&format=json`
        );
        const data = await response.json();
        // Update location name based on available fields
        this.city =
          data.address.city ||
          data.address.town ||
          data.address.village ||
          "Unknown city";
        this.state = data.address.state || null;
        this.country = data.address.country || "Unknown country";
        this.currentLocation = this.state
          ? `${this.city}, ${this.state}, ${this.country}`
          : `${this.city}, ${this.country}`;
      } catch (error) {
        console.error("Error fetching location:", error);
        this.currentLocation = "Unknown location";
      }
    },

    async handleSearch(query) {
      try {
        const locations = await geocodingService.searchLocations(query);
        if (locations.length > 0) {
          const location = locations[0];
          this.latitude = location.latitude;
          this.longitude = location.longitude;
          await this.fetchWeatherData();

          // Fetch and update the city name
          await this.fetchCityName();
          console.log("Updated City Name:", this.currentLocation);
        }
      } catch (error) {
        console.error("Error searching location:", error);
      }
    },

    async getLocation() {
      try {
        const position = await this.getUserLocation();
        this.latitude = position.coords.latitude;
        this.longitude = position.coords.longitude;
        await this.fetchWeatherData();
      } catch (error) {
        console.error("Error getting location:", error);
        alert(
          "Could not get your location. Please use the search bar instead."
        );
      }
    },

    getUserLocation() {
      return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
          reject(new Error("Geolocation is not supported by your browser"));
        }
        navigator.geolocation.getCurrentPosition(resolve, reject);
      });
    },

    formatTime(isoString) {
      return new Date(isoString).toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
      });
    },
  },

  mounted() {
    this.fetchDataFromJson();
    console.log(this);
    // this.getLocation().then(() => {
    //   // Call fetchCityName after location has been set
    //   this.fetchCityName().then(() => {
    //     console.log("Current Location:", this.currentLocation);
    //   });
    // });
  },
};
</script>

<style scoped>
.weather-app {
  font-family: Arial, sans-serif;
  color: white;
  background-color: #1e1e1e;
  padding: 0 20px 20px 20px;
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

.current-weather,
.weekly-forecast,
.supplementary-conditions,
.updated-user-forecast {
  background-color: #34495e;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 5px;
}

.current-weather {
  text-align: center;
  display: flex;
  flex-direction: column; /* Stack elements vertically */
  align-items: center; /* Center child elements horizontally */
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

.location-btn,
.update-btn {
  background-color: #3498db;
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s;
  margin-right: 10px;
}

.location-btn:hover,
.update-btn:hover {
  background-color: #2980b9;
}

.search-section {
  margin-bottom: 20px;
}

.sun-times {
  background-color: #34495e;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 5px;
}

.weather-icon {
  width: 80px;
  height: 80px;
  margin-right: 20px;
}

.loc {
  text-align: right;
  padding-right: 5%;
  font-size: smaller;
}

.header-row {
  display: flex;
  align-items: baseline; /* Vertically align items */
  gap: 8px; /* Add space between h2 and h4 */
}
</style>
