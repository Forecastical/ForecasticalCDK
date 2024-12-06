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

        <!-- New AI Prediction Status Window -->
        <div v-if="taggingInProgress || latestTagging" class="prediction-window">
          <div class="prediction-header">
            <h3>AI Weather Analysis</h3>
          </div>
          
          <div class="prediction-content">
            <template v-if="taggingInProgress">
              <div class="prediction-loading">
                <div class="spinner"></div>
                <p>Analyzing weather conditions...</p>
              </div>
            </template>
            
            <template v-else-if="latestTagging">
              <div class="prediction-result">
                <div class="prediction-item">
                  <span class="prediction-label">Weather Condition:</span>
                  <span class="prediction-value">{{ latestTagging.prediction }}</span>
                </div>
              </div>
            </template>
          </div>
        </div>

        <div v-if="loading" class="loading">
          Loading weather feed...
        </div>

        <div v-else-if="error" class="error">
          {{ error }}
        </div>
        
        <div v-else-if="posts.length === 0" class="no-images">
          No weather images yet. Be the first to share!
        </div>
        <WeatherFeedGrid v-else :posts="posts" @post-deleted="handleDeletedPost" />
      </div>
    </div>
  </div>
</template>

<script>
import ImageUpload from './ImageUpload.vue';
import WeatherFeedGrid from './WeatherFeedGrid.vue';
import { weatherFeedService } from '@/services/weatherFeedService';

export default {
  name: 'WeatherFeed',
  components: {
    ImageUpload,
    WeatherFeedGrid
  },

  data() {
    return {
      currentIndex: 0,
      showUpload: false,
      loading: true,
      error: null,
      posts: [],
      latestTagging: null, // Add this line
      taggingInProgress: false,
      //[
      //  { 
      //    image: "https://raw.githubusercontent.com/yavuzceliker/sample-images/refs/heads/main/images/image-100.jpg",
      //    location: 'New York',
      //    created_at: '2021-07-01T12:00:00Z',
      //    username: 'johndoe',
      //    caption: 'Beautiful day in the city!',
      //    weather_prediction: 'Sunny'
      //  },
      //  { 
      //    image: "https://raw.githubusercontent.com/yavuzceliker/sample-images/refs/heads/main/images/image-101.jpg",
      //    location: "San Francisco",
      //    created_at: '2021-07-02T09:30:00Z',
      //    username: "janedoe",
      //    caption: "Golden Gate Bridge",
      //    weather_prediction: "Foggy"
      //  },
      //  {
      //    image: "https://raw.githubusercontent.com/yavuzceliker/sample-images/refs/heads/main/images/image-102.jpg",
      //    location: "Paris",
      //    created_at: '2021-07-03T15:45:00Z',
      //    username: "johndoe",
      //    caption: "Eiffel Tower",
      //    weather_prediction: "Rainy"
      //  }
      //]
    };
  },

  computed: {
  },

  methods: {
    async handleDeletedPost() {
      console.log("handleDeletedPost");
      await this.fetchPosts();
    },
    
    async fetchPosts() {
      console.log('Fetching weather feed...');
      this.loading = true;
      this.error = null;

      try {
        const response = await weatherFeedService.getFeedImages();
        this.posts = response.images;
        
        // If there are posts, trigger background tagging
        if (this.posts.length > 0) {
          this.processLatestUntaggedImage();
        }
      } catch (error) {
        console.error('Error fetching images:', error);
        this.error = 'Failed to load weather feed. Please try again later.';
      } finally {
        this.loading = false;
      }
    },

    async processLatestUntaggedImage() {
      if (this.taggingInProgress) return;

      const untaggedPost = this.posts.find(post => !post.weather_prediction);
      if (!untaggedPost) {
        console.log('No untagged images found');
        return;
      }

      console.log('Processing untagged image:', untaggedPost.id);
      this.taggingInProgress = true;
      try {
        const tagResult = await weatherFeedService.tagLatestImage(untaggedPost.url);
        console.log('Image tagging result:', tagResult);
        
        if (tagResult && tagResult.prediction) {
          untaggedPost.weather_prediction = tagResult.prediction;
          this.latestTagging = tagResult; // Store the full tag result
          console.log('Updated weather prediction:', untaggedPost.weather_prediction);
        }
      } catch (tagError) {
        console.error('Error tagging image:', tagError);
      } finally {
        this.taggingInProgress = false;
      }
    },

    async handleNewImage() {
      try {
        await this.fetchPosts();
        this.currentIndex = 0; // Show the newest image
        this.showUpload = false; // Hide the upload form
      } catch (error) {
        console.error('Error refreshing feed:', error);
      }
    },

    toggleUpload() {
      this.showUpload = !this.showUpload;
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
    await this.fetchPosts();
  },

  beforeUnmount() {
    // Clean up any resources if needed
  }
};
</script>


<style scoped>

/* Add these new styles */
.prediction-window {
  background-color: #2c3e50;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.prediction-header {
  background-color: #34495e;
  padding: 15px 20px;
  border-bottom: 1px solid #405468;
}

.prediction-header h3 {
  color: #50e2e7;
  margin: 0;
  font-size: 1.2em;
}

.prediction-content {
  padding: 20px;
}

.prediction-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  color: #bdc3c7;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #50e2e7;
  border-top: 3px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.prediction-result {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.prediction-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #405468;
}

.prediction-label {
  color: #bdc3c7;
  font-size: 0.9em;
}

.prediction-value {
  color: #50e2e7;
  font-weight: bold;
  font-size: 1.1em;
}


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
