import Vue from 'vue';
import Router from 'vue-router';
import DormFilter from './components/DormsComponents/DormFilter/DormFilter.vue';
import Login from './components/ReservationComponents/Login/Login.vue'
import Reservation from './components/ReservationComponents/ReservationProcess/ReservationProcess.vue'
import DormProfile from './components/SingleDormComponents/DormProfile/DormProfile.vue'
import DormManager from './components/ManagerComponents/DormManager/DormManager.vue'
import store from './store'

Vue.use(Router)

let router = new Router({
  routes: [
    {
      path: '/',
      component: DormFilter
    },
    {
      path: '/login',
      component: Login,
      beforeEnter: (to, from, next) => { (store.getters.isLoggedIn) ? next('/') : next() }
    },
    {
      path: '/reservation',
      component: Reservation
    },
    {
      path: '/dorms/:id',
      component: DormProfile,
    },
    {
      path: '/manage',
      component: DormManager,
      beforeEnter: (to, from, next) => { (store.getters.isAdmin) ? next() : next('/login') }
    },
  ],
  mode: 'history',
  scrollBehavior() {
    return { x: 0, y: 0 }
  }
})

export default router