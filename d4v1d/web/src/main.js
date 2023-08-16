import './assets/base.css'

import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons'

const app = createApp(App)

app.use(router)
library.add(faMagnifyingGlass)
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')
