<template>
  <div class="map-card">
    <h3>Weather Map</h3>
    <div id="map"></div>
    <button @click="getCurrentLocation" class="location-button">
      Current Location
    </button>
    <div class="layer-controls">
      <button @click="toggleLayer('temperature')" class="weather-button">Temperature</button>
      <button @click="toggleLayer('precipitation')" class="weather-button">Precipitation</button>
      <button @click="toggleLayer('cloud')" class="weather-button">Clouds</button>
    </div>
  </div>
</template>

<script>
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import XYZ from 'ol/source/XYZ';
import { fromLonLat } from 'ol/proj';

export default {
  name: 'MapCard',
  data() {
    return {
      map: null,
      apiKey: '7a6af2ce40a562860a6d31c50aff2568',
      weatherLayers: {
        temperature: null,
        precipitation: null,
        cloud: null
      }
    };
  },
  mounted() {
    // Create weather layers
    const temperatureLayer = new TileLayer({
      source: new XYZ({
        url: `https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=${this.apiKey}`,
        opacity: 0.6
      })
    });

    const precipitationLayer = new TileLayer({
      source: new XYZ({
        url: `https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=${this.apiKey}`,
        opacity: 0.6
      })
    });

    const cloudLayer = new TileLayer({
      source: new XYZ({
        url: `https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=${this.apiKey}`,
        opacity: 0.6
      })
    });

    // Store layers for later use
    this.weatherLayers = {
      temperature: temperatureLayer,
      precipitation: precipitationLayer,
      cloud: cloudLayer
    };

    // Initialize map with base and weather layers
    this.map = new Map({
      target: 'map',
      layers: [
        new TileLayer({
          source: new OSM()
        }),
        temperatureLayer,    // Add weather layers
        precipitationLayer,
        cloudLayer
      ],
      view: new View({
        center: [0, 0],
        zoom: 2,
      }),
    });
  },
  methods: {
    getCurrentLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            const coordinates = fromLonLat([longitude, latitude]);
            
            this.map.getView().animate({
              center: coordinates,
              zoom: 13,
              duration: 1000
            });
          },
          () => {
            console.log("Unable to retrieve your location");
          }
        );
      } else {
        console.log("Geolocation not supported");
      }
    },
    // Optional: Methods to toggle weather layers
    toggleLayer(layerName) {
      if (this.weatherLayers[layerName]) {
        this.weatherLayers[layerName].setVisible(!this.weatherLayers[layerName].getVisible());
      }
    }
  }
};
</script>

<style scoped>
.map-card {
  position: absolute;
  top: 85%;
  right: 2%;
  width: 300px;
  height: 300px;
  border: .5px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
}

#map {
  width: 100%;
  height: 100%;
}

.layer-controls {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.location-button {
  position: absolute;
  top: 85%;
  right: 2%;
  width: 100px;
  height: 40px;
  border: .5px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  background-color: white;
}
</style>