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
      apiKey: process.env.VUE_APP_OPEN_WEATHER_API_KEY,
      weatherLayers: {
        temperature: null,
        precipitation: null,
        cloud: null
      }
    };
  },
  mounted() {
    // Setup the 3 weather layers: temp, precipitation, and cloud cover
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

    this.weatherLayers = {
      temperature: temperatureLayer,
      precipitation: precipitationLayer,
      cloud: cloudLayer
    };

    // Build map using the weather layers defined above
    this.map = new Map({
      target: 'map',
      layers: [
        new TileLayer({
          source: new OSM()
        }),
        temperatureLayer,
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

    // geolocating method to get the location of user
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
            console.log("Could not retrieve location");
          }
        );
      } else {
        console.log("Geolocation is unsupported");
      }
    },
    
    // method giving the ability to toggle between the individual weather layers
    toggleLayer(layer) {
      if (this.weatherLayers[layer]) {
        this.weatherLayers[layer].setVisible(!this.weatherLayers[layer].getVisible());
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