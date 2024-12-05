import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/lib/components'
import * as directives from 'vuetify/lib/directives'
import { VueMasonryPlugin } from 'vue-masonry'
import mitt from 'mitt'

const emitter = mitt()
const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(createVuetify({
  theme: {
    dark: true
  },
  components,
  directives
}))
app.config.globalProperties.emitter = emitter
app.use(VueMasonryPlugin)
app.mount('#app')
