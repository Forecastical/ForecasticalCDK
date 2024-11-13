// ImageUpload.vue
<template>
  <div class="upload-container">
    <div 
      class="upload-area"
      @dragover.prevent="handleDragOver"
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
    >
      <input 
        type="file"
        ref="fileInput"
        class="hidden-input"
        accept="image/*"
        @change="handleFileSelect"
      />
      
      <div v-if="!preview" class="upload-placeholder">
        <span class="upload-icon">📸</span>
        <p class="upload-text">Drag and drop an image or click to upload</p>
        <p class="upload-subtext">Supported formats: JPG, PNG, WEBP</p>
      </div>
      
      <img v-else :src="preview" alt="Preview" class="image-preview" />
    </div>

    <div v-if="preview" class="upload-form">
      <input 
        v-model="caption"
        type="text"
        placeholder="Add a caption..."
        class="caption-input"
      />
      
      <div class="button-group">
        <button @click="cancelUpload" class="cancel-btn">Cancel</button>
        <button @click="submitUpload" class="submit-btn">Share Photo</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ImageUpload',
  data() {
    return {
      file: null,
      preview: null,
      caption: ''
    }
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    
    handleDragOver(e) {
      e.target.classList.add('drag-over');
    },
    
    handleDrop(e) {
      e.target.classList.remove('drag-over');
      const file = e.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) {
        this.processFile(file);
      }
    },
    
    handleFileSelect(e) {
      const file = e.target.files[0];
      if (file) {
        this.processFile(file);
      }
    },
    
    processFile(file) {
      this.file = file;
      const reader = new FileReader();
      reader.onload = (e) => {
        this.preview = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    
    cancelUpload() {
      this.file = null;
      this.preview = null;
      this.caption = '';
      this.$refs.fileInput.value = '';
    },
    
    submitUpload() {
      if (!this.file || !this.caption) return;
      
      // Create a new weather post object
      const newPost = {
        url: this.preview,
        caption: this.caption,
        username: 'currentUser', // You'll want to get this from your auth system
        location: 'Cleveland, OH', // You'll want to get this from geolocation
        time: 'Just now'
      };
      
      // Emit the new post to parent component
      this.$emit('image-uploaded', newPost);
      
      // Reset the form
      this.cancelUpload();
    }
  }
}
</script>

<style scoped>
.upload-container {
  margin: 20px 0;
}

.upload-area {
  position: relative;
  width: 100%;
  height: 300px;
  border: 2px dashed #50e2e7;
  border-radius: 10px;
  background-color: rgba(80, 226, 231, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
}

.upload-area:hover {
  background-color: rgba(80, 226, 231, 0.15);
}

.upload-area.drag-over {
  background-color: rgba(80, 226, 231, 0.2);
  border-color: #3dd8dd;
}

.hidden-input {
  display: none;
}

.upload-placeholder {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #50e2e7;
}

.upload-icon {
  font-size: 3em;
  margin-bottom: 10px;
  display: block;
}

.upload-text {
  font-size: 1.2em;
  margin: 0 0 10px 0;
}

.upload-subtext {
  font-size: 0.9em;
  color: #bdc3c7;
}

.image-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-form {
  margin-top: 20px;
}

.caption-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #34495e;
  border-radius: 5px;
  background-color: #2c3e50;
  color: white;
  margin-bottom: 15px;
}

.button-group {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.cancel-btn, .submit-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: all 0.3s ease;
}

.cancel-btn {
  background-color: transparent;
  color: #bdc3c7;
  border: 1px solid #34495e;
}

.cancel-btn:hover {
  background-color: rgba(52, 73, 94, 0.5);
}

.submit-btn {
  background-color: #50e2e7;
  color: #1e1e1e;
}

.submit-btn:hover {
  background-color: #3dd8dd;
  transform: translateY(-1px);
}
</style>