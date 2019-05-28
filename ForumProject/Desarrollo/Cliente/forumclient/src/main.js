import Vue from 'vue'
import Vuetify from 'vuetify'
import './plugins/vuetify'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'

Vue.config.productionTip = false

Vue.use(Vuetify, {
  options: {
    themeVariations: ['primary', 'secondary', 'accent'],
    extra: {
      mainToolbar: {
        color: 'primary'
      },
      sideToolbar: {
      },
      sideNav: 'primary',
      mainNav: 'primary lighten-1',
      bodyBg: ''
    }
  }
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
