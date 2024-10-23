<template>
  <div class="map-card">
    <h3>Weather Map</h3>
    <div id="map"></div>
    <button @click="getCurrentLocation" class="location-button">
      Current Location
    </button>
  </div>
</template>

<script>
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import { fromLonLat } from 'ol/proj';

export default {
  name: 'MapCard',
  data() {
    return {
      map: null,
    };
  },
  mounted() {
    this.map = new Map({
      target: 'map',
      layers: [
        new TileLayer({
          source: new OSM(),
        }),
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
            
            // Center map on location
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
    }
  },  
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

.location-button{
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