<template>
  <div class="weather-app">
    <div class="content">
      <div class="feed-container">
        <div class="feed-header">
          <h2 class="title">Weather Feed</h2>
          <button @click="toggleUpload" class="update-btn">
            <span class="icon">📸</span>
            Share Weather
          </button>
        </div>
        
        <ImageUpload 
          v-if="showUpload"
          @image-uploaded="handleNewImage"
        />

        <div v-if="loading" class="loading">
          Loading weather feed...
        </div>

        <div v-else-if="error" class="error">
          {{ error }}
        </div>
        
        <div v-else-if="images.length === 0" class="no-images">
          No weather images yet. Be the first to share!
        </div>

        <div v-else class="feed-card">
          <div class="image-container">
            <img :src="currentImage.url" :alt="currentImage.caption" class="feed-image" />
            <div class="navigation-buttons">
              <button @click="previousImage" class="nav-btn" :disabled="loading">←</button>
              <button @click="nextImage" class="nav-btn" :disabled="loading">→</button>
            </div>
          </div>
          
          <div class="caption-container">
            <p class="caption">{{ currentImage.caption }}</p>
            <div class="metadata">
              <span class="username">{{ currentImage.username }}</span>
              <span class="location-time">
                {{ currentImage.location }} • {{ formatTime(currentImage.created_at) }}
              </span>
            </div>
            <div v-if="currentImage.weather_prediction" class="weather-info">
              <span class="weather-label">Weather Prediction:</span>
              <span class="weather-value">{{ currentImage.weather_prediction }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ImageUpload from './ImageUpload.vue';
import { weatherFeedService } from '@/services/weatherFeedService';

export default {
  name: 'WeatherFeed',
  components: {
    ImageUpload
  },

  data() {
    return {
      currentIndex: 0,
      showUpload: false,
      loading: true,
      error: null,
      images: []
    };
  },

  computed: {
    currentImage() {
      if (!this.images[this.currentIndex]) return {};
      const image = {...this.images[this.currentIndex]};
      // Rewrite URL to point to backend
      image.url = `http://localhost:8000${image.url}`;
      return image;
    }
  },

  methods: {
    async fetchImages() {
      this.loading = true;
      this.error = null;

      try {
        const response = await weatherFeedService.getFeedImages();
        this.images = response.images;
      } catch (error) {
        console.error('Error fetching images:', error);
        this.error = 'Failed to load weather feed. Please try again later.';
      } finally {
        this.loading = false;
      }
    },

    nextImage() {
      if (this.images.length > 0) {
        this.currentIndex = (this.currentIndex + 1) % this.images.length;
      }
    },

    previousImage() {
      if (this.images.length > 0) {
        this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
      }
    },

    toggleUpload() {
      this.showUpload = !this.showUpload;
    },

    async handleNewImage() {  // Remove the unused newPost parameter
      try {
        // Refresh the feed to get the new image
        await this.fetchImages();
        this.currentIndex = 0; // Show the newest image
        this.showUpload = false; // Hide the upload form
      } catch (error) {
        console.error('Error refreshing feed:', error);
      }
    },

    formatTime(timestamp) {
      if (!timestamp) return '';

      const date = new Date(timestamp);
      const now = new Date();
      const diffInSeconds = Math.floor((now - date) / 1000);

      if (diffInSeconds < 60) {
        return 'Just now';
      } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60);
        return `${minutes} ${minutes === 1 ? 'minute' : 'minutes'} ago`;
      } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600);
        return `${hours} ${hours === 1 ? 'hour' : 'hours'} ago`;
      } else {
        const days = Math.floor(diffInSeconds / 86400);
        return `${days} ${days === 1 ? 'day' : 'days'} ago`;
      }
    }
  },

  async mounted() {
    await this.fetchImages();
  },

  beforeUnmount() {
    // Clean up any resources if needed
  }
};
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

.loading {
  text-align: center;
  padding: 40px;
  color: #50e2e7;
  background-color: #34495e;
  border-radius: 10px;
  margin-bottom: 20px;
}

.error {
  text-align: center;
  padding: 20px;
  color: #e74c3c;
  background-color: #34495e;
  border-radius: 10px;
  margin-bottom: 20px;
}

.no-images {
  text-align: center;
  padding: 40px;
  color: #bdc3c7;
  background-color: #34495e;
  border-radius: 10px;
  margin-bottom: 20px;
}

.weather-info {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #405468;
  color: #bdc3c7;
}

.weather-label {
  color: #50e2e7;
  margin-right: 8px;
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}
</style>
