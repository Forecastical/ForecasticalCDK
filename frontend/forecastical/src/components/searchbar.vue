<template>
  <div>
    <input 
        type="text"
        v-model="searchQuery"
        @input="onSearch"
        placeholder="Search for a city..."
    />
  </div>
</template>


<script>
export default {
  data() {
    return {
      searchQuery: "",
    };
  },
  methods: {
    onSearch() {
      this.$emit("search", this.searchQuery);
    },
  },
};
</script>

<style scoped>

input {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 100%;
}



</style>