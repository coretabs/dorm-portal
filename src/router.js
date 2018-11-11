import Vue from 'vue'
import Router from 'vue-router'
import DormFilter from './components/dorms/DormFilter'
import Login from './components/reservation/login/Login'
import Reservation from './components/reservation/reservationProcess/ReservationProcess'

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
