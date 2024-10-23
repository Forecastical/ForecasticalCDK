<template>
  <div class="weather-app">
    <div class="content">
      <div class="feed-container">
        <div class="feed-header">
          <h2 class="title">Weather Feed</h2>
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
              <span class="location-time">{{ currentImage.location }} • {{ currentImage.time }}</span>
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
      console.log('Updating location...');
    }
  }
}
</script>

<style scoped>
.weather-app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px 20px 20px;
}

.title {
  color: #50e2e7;
  font-size: 1.8em;
  margin: 0;
}

.feed-container {
  width: 100%;
}

.feed-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.feed-card {
  background-color: #2c3e50;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.image-container {
  position: relative;
  width: 100%;
  height: 500px;
  background-color: #34495e;
}

.feed-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
  background-color: #50e2e7;
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
  transition: all 0.3s ease;
  opacity: 0.9;
}

.nav-btn:hover {
  opacity: 1;
  transform: scale(1.1);
}

.caption-container {
  padding: 20px;
  background-color: #34495e;
}

.caption {
  font-size: 1.2em;
  margin: 0 0 15px 0;
  color: white;
}

.metadata {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid #405468;
}

.username {
  color: #50e2e7;
  font-weight: bold;
}

.location-time {
  color: #bdc3c7;
}

.update-btn {
  background-color: #50e2e7;
  border: none;
  color: #1e1e1e;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.update-btn:hover {
  background-color: #3dd8dd;
  transform: translateY(-1px);
}

.icon {
  font-size: 1.2em;
}

@media (max-width: 768px) {
  .feed-container {
    padding: 0;
  }
  
  .feed-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .image-container {
    height: 300px;
  }
  
  .nav-btn {
    width: 36px;
    height: 36px;
  }
}
</style>