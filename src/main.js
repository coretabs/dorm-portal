import 'babel-polyfill'
import Vue from 'vue'
import '@/plugins/vuetify'
import App from '@/App.vue'
import router from '@/router'
import store from "@/store"
import $backend from '@/backend'
import VueCookie from 'vue-cookie'
import Vuetify from 'vuetify'
Vue.prototype.$backend = $backend
Vue.config.productionTip = false
import 'vuetify/dist/vuetify.min.css' 
Vue.use(Vuetify)
Vue.use(VueCookie)

const vue = new Vue({
  router,
  store,
  render: h => h(App)
})

vue.$mount('#app')


