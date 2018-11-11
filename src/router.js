import Vue from 'vue';
import Router from 'vue-router';
import DormFilter from './components/dorms/DormFilter/DormFilter.vue';
import Login from './components/reservation/Login/Login.vue';
import Reservation from './components/reservation/ReservationProcess/ReservationProcess.vue';

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
