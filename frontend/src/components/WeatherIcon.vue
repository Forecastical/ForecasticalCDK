<template>
    <div class="weather-icon">
      <component 
        :is="iconComponent"
        :size="size"
        :color="color"
        :stroke-width="strokeWidth"
      />
    </div>
  </template>
  
  <script>
  import {
    Sun,
    Cloud,
    CloudRain,
    CloudSnow,
    CloudFog,
    CloudLightning,
    CloudDrizzle,
    CloudOff,
    Cloudy
  } from 'lucide-vue-next';
  
  export default {
    name: 'WeatherIcon',
    
    components: {
      Sun,
      Cloud,
      CloudRain,
      CloudSnow,
      CloudFog,
      CloudLightning,
      CloudDrizzle,
      CloudOff,
      Cloudy
    },
  
    props: {
      code: {
        type: Number,
        required: true
      },
      size: {
        type: Number,
        default: 48
      },
      color: {
        type: String,
        default: '#50e2e7'
      },
      strokeWidth: {
        type: Number,
        default: 2
      }
    },
  
    computed: {
      iconComponent() {
        switch (this.code) {
          case 0: // Clear
            return 'Sun';
          
          case 1: // Mainly clear
            return 'Sun';
          
          case 2: // Partly cloudy
            return 'Cloudy';
          
          case 3: // Overcast
            return 'Cloud';
          
          case 45: // Foggy
          case 48: // Depositing rime fog
            return 'CloudFog';
          
          case 51: // Light drizzle
          case 53: // Moderate drizzle
          case 55: // Dense drizzle
            return 'CloudDrizzle';
          
          case 56: // Light freezing drizzle
          case 57: // Dense freezing drizzle
            return 'CloudSnow';
          
          case 61: // Slight rain
          case 63: // Moderate rain
          case 65: // Heavy rain
            return 'CloudRain';
          
          case 66: // Light freezing rain
          case 67: // Heavy freezing rain
            return 'CloudSnow';
          
          case 71: // Snow fall: Slight
          case 73: // Snow fall: Moderate
          case 75: // Snow fall: Heavy
          case 77: // Snow grains
            return 'CloudSnow';
          
          case 80: // Rain showers: Slight
          case 81: // Rain showers: Moderate
          case 82: // Rain showers: Violent
            return 'CloudRain';
          
          case 85: // Snow showers slight
          case 86: // Snow showers heavy
            return 'CloudSnow';
          
          case 95: // Thunderstorm: Slight or moderate
          case 96: // Thunderstorm with slight hail
          case 99: // Thunderstorm with heavy hail
            return 'CloudLightning';
          
          default:
            return 'CloudOff';
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .weather-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  </style>
