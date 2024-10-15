<template>
    <div class="map-card">
      <h3>Weather Map</h3>
      <div id="map"></div>
    </div>
</template>







<style scoped>
.map-card {
  position: absolute;
  top: 85%;
  right: 2%;
  width: 300px; 
  height: 300px; 
  border: 1px solid #ccc; 
  border-radius: 8px; 
  overflow: hidden; 
}
#map {
  width: 100%;
  height: 100%;
}
</style>