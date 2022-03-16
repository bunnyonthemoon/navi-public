import { createApp } from 'vue'
import template from './app.vue'
import { createMetaManager } from 'vue-meta'

const App = createApp(template)


import store from '@/store'
App.use(store)

import router from '@/router'
App.use(router)


import VueGoogleMaps from '@fawmi/vue-google-maps'
App.use(VueGoogleMaps, {
    load: {
        key: 'AIzaSyDyiRlkTZJjQ8N1jG0XsLCgXHKaESK1Qfs',
        language: 'ru',
    },
})


import Axios from 'axios'
import Cookies from 'js-cookie'
Axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')


import '@/styles/base.styl'


import globalComponents from '@/global'
globalComponents(App)

const metaManager = createMetaManager()

App.use(metaManager)
// App.use(metaPlugin)


App.mount('#app')
export default App
