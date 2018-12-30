import Vue from 'vue';
import Router from 'vue-router';
import DormFilter from './components/DormsComponents/DormFilter/DormFilter.vue';
import Login from './components/ReservationComponents/Login/Login.vue'
import Reservation from './components/ReservationComponents/ReservationProcess/ReservationProcess.vue'
import DormProfile from './components/SingleDormComponents/DormProfile/DormProfile.vue'
import DormManager from './components/ManagerComponents/DormManager/DormManager.vue'
import ConfirmAccount from './components/ReservationComponents/ConfirmAccount/ConfirmAccount.vue'
import ResetPassword from './components/ReservationComponents/ResetPassword/ResetPassword.vue'
import ReviewDorm from './components/DormsComponents/ReviewDorm/ReviewDorm.vue'

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
      path: '/reservations/:id/review',
      component: ReviewDorm,
      beforeEnter: (to, from, next) => { (store.getters.isLoggedIn) ? next() : next('/login') }
    },
    {
      path: '/reservation',
      component: Reservation
    },
    {
      path: '/dorms/:id',
      component: DormProfile
    },
    {
      path: '/confirm-account/:key',
      component: ConfirmAccount
    },
    {
      path: '/manage',
      component: DormManager,
      beforeEnter: (to, from, next) => { (store.getters.isAdmin) ? next() : next('/login') }
    },
    {
      path: '/reset-password/:id/:key',
      component: ResetPassword
    }
  ],
  mode: 'history',
  scrollBehavior() {
    return { x: 0, y: 0 }
  }
})

export default router