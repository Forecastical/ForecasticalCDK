<template>
  <v-img :src="image_url" class="weather-image" />
</template>

<script>
export default {
  name: 'WeatherImage',
  props: {
    url: {
      type: String,
      required: true
    }
  },
  computed: {
  },
  data() {
    return {
      image_url: "http://localhost:8000" + this.url
    };
  },
}
</script>
