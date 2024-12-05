//WeatherFeedGrid.vue
<template>
  <v-masonry
    :cols="{ default: 4, 1100: 3, 700: 2, 500: 1 }"
    gutter="30px"
    class="masonry-container"
    fit-width="true"
  >
    <v-masonry-tile v-for="post in posts" :key="post.id" class="masonry-tile">
      <v-card class="md-card">
        <WeatherImage :url="post.url" />
        <v-card-title>
          <span class="caption">{{post.caption}}</span>
        </v-card-title>
        <v-card-subtitle>
          <span>{{post.weather_prediction}}</span>
        </v-card-subtitle>
        
        <v-card-text>
          <v-row>
            <v-col cols="3">
              <span>@{{ post.username }}</span>
            </v-col>
            <v-col cols="7" align="right">
              <!-- make this text align to the right -->
              <div class="location-time">{{post.location}}</div>
              <div class="location-time">{{formatTime(post.created_at)}}</div>
            </v-col>
          </v-row>
        </v-card-text>
        <!-- Buttons -->
        <v-card-actions>
          <v-btn @click="clickComment" >
            <svg-icon color="cyan" type="mdi" :path="commentIcon"></svg-icon>
          </v-btn>
          <v-btn icon @click="clickEdit">
            <svg-icon color="cyan" type="mdi" :path="editIcon"></svg-icon>
          </v-btn>
          <v-btn icon @click="clickDelete">
            <svg-icon color="cyan" type="mdi" :path="deleteIcon"></svg-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-masonry-tile>
  </v-masonry>
</template>
<script>
import SvgIcon from '@jamescoyle/vue-icon';
import WeatherImage from './WeatherImage.vue';
import { mdiComment, mdiPencil, mdiTrashCanOutline } from '@mdi/js';
//import WeatherFeedCard from './WeatherFeedCard.vue';
  //<WeatherFeedCard :image="post.image" :location="post.location" :created_at="post.created_at" :username="post.username" :caption="post.caption" :weather_prediction="post.weather_prediction" />
// currentImage.weather_prediction
// currentImage.location
// currentImage.created_at
// currentImage.username
// currentImage.caption
export default {
  name: 'WeatherFeedGrid',
  components: {
    SvgIcon,
    WeatherImage
  },
  props: {
    posts: {
      type: Array,
      required: true
    },
  },
  data() {
    return {
      currentImageIndex: 0,
      loading: false,
      commentIcon: mdiComment,
      editIcon: mdiPencil,
      deleteIcon: mdiTrashCanOutline
    }
  },
  computed: {
  },
  methods: {
    previousImage() {
      if (this.currentImageIndex > 0) {
        this.currentImageIndex--;
      }
    },
    nextImage() {
      if (this.currentImageIndex < this.images.length - 1) {
        this.currentImageIndex++;
      }
    },
    formatTime(time) {
      const date = new Date(time);
      return date.toLocaleString();
    },
    getImageFromURI(uri) {
      return uri;
    },
  }
}
</script>
<style  scoped>

.v-btn {
  &:hover {
    background-color: #2c3e50;
  }
}
.location-time {
  text-align: right; /* Align text within the element to the right */
}
  .md-card {
    width: 320px;
    margin: 4px;
    display: inline-block;
    vertical-align: top;
    background-color: #2c3e50;
    color: #bdc3c7;
  }

  .md-card-example {
    .md-subhead {
      .md-icon {
        $size: 16px;

        width: $size;
        min-width: $size;
        height: $size;
        font-size: $size !important;
      }

      span {
        vertical-align: middle;
      }
    }

    .card-reservation {
      margin-top: 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;

      .md-icon {
        margin: 8px;
      }
    }

    .md-button-group {
      display: flex;

      .md-button {
        min-width: 60px;
        border-radius: 2px;
      }
    }
  }
</style>
