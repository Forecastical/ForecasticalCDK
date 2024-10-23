<template>
  <div class="weather-app">
    <div class="content">
      <div class="feed-container">
        <div class="feed-header">
          <h2>Weather Feed</h2>
          <button @click="updateLocation" class="update-btn">
            <span class="icon">↻</span>
            Update Location
          </button>
        </div>
        
        <div class="feed-card">
          <div class="image-container">
            <img :src="currentImage.url" :alt="currentImage.caption" class="feed-image" />
            <div class="navigation-buttons">
              <button @click="previousImage" class="nav-btn">←</button>
              <button @click="nextImage" class="nav-btn">→</button>
            </div>
          </div>
          
          <div class="caption-container">
            <p class="caption">{{ currentImage.caption }}</p>
            <div class="metadata">
              <span class="username">{{ currentImage.username }}</span>
              <span class="location-time">
                {{ currentImage.location }} • {{ currentImage.time }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import hurricane from '@/assets/hurricane.webp'
import partlyCloudy from '@/assets/partly_cloudy.png'
import rainy from '@/assets/rainy.png'
import sunny from '@/assets/sunny.png'

export default {
  name: 'WeatherFeed',
  data() {
    return {
      currentIndex: 0,
      images: [
        {
          url: hurricane,
          caption: 'Hurricane warning in effect',
          username: 'stormChaser',
          location: 'Cleveland, OH',
          time: '2 hours ago'
        },
        {
          url: partlyCloudy,
          caption: 'Beautiful partly cloudy day',
          username: 'skyWatcher',
          location: 'Akron, OH',
          time: '5 hours ago'
        },
        {
          url: rainy,
          caption: 'April showers bring May flowers',
          username: 'rainLover',
          location: 'Columbus, OH',
          time: '1 day ago'
        },
        {
          url: sunny,
          caption: 'Perfect sunny day for outdoor activities',
          username: 'sunSeeker',
          location: 'Cincinnati, OH',
          time: '3 hours ago'
        }
      ]
    }
  },
  computed: {
    currentImage() {
      return this.images[this.currentIndex];
    }
  },
  methods: {
    nextImage() {
      this.currentIndex = (this.currentIndex + 1) % this.images.length;
    },
    previousImage() {
      this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
    },
    updateLocation() {
      // Placeholder for location update functionality
      console.log('Updating location...');
    }
  }
}
</script>

<style scoped>
.feed-container {
  max-width: 800px;
  margin: 0 auto;
}

.feed-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.feed-card {
  background-color: #34495e;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 20px;
}

.image-container {
  position: relative;
  width: 100%;
  padding-top: 75%; /* 4:3 Aspect Ratio */
  background-color: #2c3e50;
}

.feed-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 20px;
}

.navigation-buttons {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  padding: 0 20px;
  transform: translateY(-50%);
}

.nav-btn {
  background-color: rgba(80, 226, 231, 0.8);
  border: none;
  color: #1e1e1e;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2em;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
}

.nav-btn:hover {
  background-color: rgba(80, 226, 231, 1);
}

.caption-container {
  padding: 20px;
}

.caption {
  font-size: 1.1em;
  margin-bottom: 10px;
}

.metadata {
  display: flex;
  justify-content: space-between;
  color: #bdc3c7;
  font-size: 0.9em;
}

.update-btn {
  background-color: #3498db;
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.3s;
}

.update-btn:hover {
  background-color: #2980b9;
}

.username {
  color: #50e2e7;
  font-weight: bold;
}

@media (max-width: 768px) {
  .feed-container {
    padding: 0 15px;
  }
  
  .feed-header {
    flex-direction: column;
    gap: 10px;
  }
  
  .image-container {
    padding-top: 100%; /* Square aspect ratio on mobile */
  }
}
</style>