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
      
      
      <!-- New button to fetch weather data 
      <div class="fetch-weather-data">
        <button @click="fetchWeatherData">
          Fetch Weather Data
        </button>
      </div>
      -->

      <!-- New button to fetch location data 
      <div class="fetch-weather-data">
        <button @click="getUserLocation">Get My Location</button>
      </div>
      -->

      <!-- Updated button to fetch weather data -->
      <div class="fetch-weather-data">
        <button @click="fetchWeatherData">
          Get My Location's Weather
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

    getUserLocation() {
      const apiKey = process.env.VUE_APP_API_KEY;

      fetch(`http://api.weatherapi.com/v1/ip.json?key=${apiKey}&q=auto:ip`)
        .then(response => {
          if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
          }
          return response.json();
        })
        .then(data => {
          console.log('IP Lookup API response:', data);
          
          // You can store the location information in data properties if needed
          this.userCity = data.city;
          this.userRegion = data.region;
          this.userCountry = data.country_name;
          this.userLatitude = data.lat;
          this.userLongitude = data.lon;
          
          // Print the data to the console
          //console.log('User Location:', {
          //  city: data.city,
          //  region: data.region,
          //  country: data.country_name,
          //  latitude: data.lat,
          //  longitude: data.lon
          //});
        })
        .catch(error => {
          console.error('Error fetching user location:', error);
        });
    },


    fetchWeatherData() {
      console.log("Fetching weather data...");
      const apiKey = process.env.VUE_APP_API_KEY;

      // First, get the user's location
      fetch(`http://api.weatherapi.com/v1/ip.json?key=${apiKey}&q=auto:ip`)
        .then(response => {
          if (!response.ok) {
            throw new Error(`IP Lookup API error: ${response.statusText}`);
          }
          return response.json();
        })
        .then(locationData => {
          console.log('IP Lookup API response:', locationData);
          
          // Store the location information
          this.userCity = locationData.city;
          this.userRegion = locationData.region;
          this.userCountry = locationData.country_name;
          this.userLatitude = locationData.lat;
          this.userLongitude = locationData.lon;

          // Now fetch the weather data using the obtained location
          return fetch(`https://api.weatherapi.com/v1/current.json?key=${apiKey}&q=${locationData.lat},${locationData.lon}`);
        })
        .then(response => {
          if (!response.ok) {
            throw new Error(`Weather API error: ${response.statusText}`);
          }
          return response.json();
        })
        .then(weatherData => {
          console.log('Weather API response:', weatherData);

          // Update the weather information
          this.currentLocation = `${this.userCity}, ${this.userRegion}`;
          this.temperature = weatherData.current.temp_f; // For Fahrenheit
          this.condition = weatherData.current.condition.text;
          this.air = weatherData.current.air_quality?.us_epa_index || "N/A";
          this.uvIndex = weatherData.current.uv;
          this.humidity = weatherData.current.humidity + "%";
          this.pressure = weatherData.current.pressure_mb + " hPa";
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },

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
