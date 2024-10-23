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

