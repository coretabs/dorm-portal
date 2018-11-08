import Vue from 'vue'
import Router from 'vue-router'
import DormFilter from './components/dorms/DormFilter'
import Login from './components/reservation/Login'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: DormFilter
    },
    {
      path: '/login',
      component: Login
    },
  ],
  mode: 'history'
})
