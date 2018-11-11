import Vue from 'vue'
import Router from 'vue-router'
import DormFilter from './components/dorms/DormFilter.vue'
import Login from './components/reservation/login/Login.vue'
import Reservation from './components/reservation/reservationProcess/ReservationProcess.vue'

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
    {
      path: '/reservation',
      component: Reservation
    },
  ],
  mode: 'history'
})
