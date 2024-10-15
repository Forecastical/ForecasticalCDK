<template>
    <div class="map-card">
      <h3>Weather Map</h3>
      <div id="map"></div>
    </div>
</template>


<script>
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';

export default {
  name: 'MapCard',
  data() {
    return {
      map: null, // Declare a variable to hold the map instance
    };
  },
  mounted() {
    // Initialize the map and assign it to the data property
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
</style>