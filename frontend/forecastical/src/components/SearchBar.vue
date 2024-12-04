<template>

  <h2>Search Location</h2>
  <div class="input-group">
    <div class="search-input">
      <input type="text" v-model="searchQuery" placeholder="Enter city name..." />
      <button @click="searchLocation" class="btn" :disabled="loading">
        {{ loading ? 'Searching...' : 'Search' }}
      </button>
    </div>
  </div>
  <div v-if="error" class="error">
    Error: {{ error }}
  </div>
  <div v-if="results" class="results">
    <h3>Search Results:</h3>
    <div class="location-results">
      <div v-for="location in results" :key="location.id" 
           class="location-item" @click="selectLocation(location)">
        <h4>{{ location.name }}</h4>
        <p>{{ location.admin1 }}, {{ location.country }}</p>
        <p class="coordinates">{{ location.latitude }}, {{ location.longitude }}</p>
      </div>
    </div>
  </div>

</template>


<script>
import { geocodingService } from '@/services/geocodingApi';

export default {
name: 'WeatherApiTest',

data() {
return {

  latitude: 41.4995,  // Default is Cleveland, OH
  longitude: -81.6954,
  searchQuery: '',
  loading: false,
  error: null,
  results: null
  };
},

methods: {
  async searchLocation() {
      if (!this.searchQuery.trim()) return;
      
      this.loading = true;
      this.error = null;
      this.results = null;

      try {
          const results = await geocodingService.searchLocations(this.searchQuery);
          this.results = results;
          if (results.length === 0) {
              this.error = 'No locations found';
          }
      } catch (error) {
      console.error('Error searching location:', error);
      this.error = 'Error searching location';
      } finally {
      this.loading = false;
      }
},

async selectLocation(location) {
  this.latitude = location.latitude;
  this.longitude = location.longitude;
  this.$emit("location-selected", location);

},

}
};
</script>


<style scoped>
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

</style>
