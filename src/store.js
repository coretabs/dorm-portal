import Vue from "vue";
import Vuex from "vuex";
import $backend from '@/backend';
Vue.prototype.$backend = $backend;

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    language: localStorage.getItem('lang') || "en",
    currencyCode: localStorage.getItem('currency-code') || "USD",
    currencySymbol: localStorage.getItem('currency-symbol') || "$",
    drawer: null,
    currencies: [],
    languages: [],
    filters: [],
    dorms:[],
    reservation: {},
    authStatus: '',
    isAuth: localStorage.getItem('auth'),
    isAdmin: localStorage.getItem('admin')
  },
  getters:{
    lang: state => {
      const currentLang = state.language
      const lang = require(`../locale/student.${currentLang}.json`);
      return lang[currentLang]
    },
    activeCurrency: state => {
      return state.currencySymbol;
    },
    isLoggedIn: state => !!state.isAuth,
    isAdmin: state => !!state.isAdmin,
    authStatus: state => state.authStatus
  },
  mutations: {
    fetchLocale(state){
      $backend.$fetchLocale().then(responseDate => {
        state.currencies = responseDate[0].currencies;
        state.languages = responseDate[1].languages;
        localStorage.setItem("lang", responseDate[1].languages[0].code);
        localStorage.setItem("currency-code", responseDate[0].currencies[0].code);
        localStorage.setItem("currency-symbol", responseDate[0].currencies[0].symbol);
      });
    },
    fetchFilters(state){
      $backend.$fetchFilters(state.language, state.currencyCode).then(responseDate => {
        state.filters = responseDate;
      });
    },
    fetchDorms(state) {
      $backend.$fetchDorms().then(responseDate => {
        state.dorms = responseDate;
      });
    },
    auth_success(state){
      state.authStatus = 'Success'
      state.isAuth = !!localStorage.getItem('auth')
      state.isAdmin = localStorage.getItem('admin')
    },
    auth_error(state){
      state.authStatus = 'An error occur'
    },
    logout(state){
      state.isAuth = null
      state.isAdmin = null
    },
    registerSuccess(state){
      state.authStatus = 'Registeration Faild'
    },
    // reserveRoom(state, payload){
    //   $backend.$reserveRoom(payload).then(responseDate => {
    //   });
    // }
    fetchReservation(state){
      $backend.$fetchReservation().then(responseDate => {
        state.reservation = responseDate;
      });
    }
  },
  actions: {
    fetchLocale(context){
      context.commit('fetchLocale');
    },
    fetchFilters(context){
      context.commit('fetchFilters');
    },
    fetchDorms(context) {
      context.commit('fetchDorms');
    },
    login({commit}){

      return new Promise((resolve, reject) => {

        $backend.$login().then(responseDate => {

          if(responseDate.is_manager){
            localStorage.setItem('admin', true)
          }
          localStorage.setItem('auth', JSON.stringify({
            user_name: responseDate.name,
            reservarion_id : responseDate.reservation_id,
            current_step: responseDate.current_step
          }))
          commit('auth_success')
          resolve(responseDate)

        })
        .catch(err => {
          localStorage.removeItem('admin')
          localStorage.removeItem('auth')
          commit('auth_error')
          reject(err)
        })


      });

    },
    logout({commit}){
      return new Promise((resolve, reject) => {
        commit('logout')
        localStorage.removeItem('auth')
        localStorage.removeItem('admin')
        resolve()
      });
    },
    reserveRoom(context,payload){

      return new Promise((resolve, reject) => {
        $backend.$reserveRoom(payload).then(responseDate => {
          //context.commit('reserveRoom')
          resolve(responseDate)
        })
        .catch(err => {
          reject(err)
        })
      });
      
    },
    fetchReservation(context){
      context.commit('fetchReservation')
    },
    register({commit}, user){
      return new Promise((resolve, reject) => {
        $backend.$register(user).then(responseDate => {
          commit('registerSuccess')
          resolve(responseDate)
        })
        .catch(err => {
          reject(err)
        })
      })
    },
    verifyEmail({commit}, key){
      return new Promise((resolve, reject) => {
        $backend.$verifyEmail(key).then(responseDate => {
          resolve(responseDate)
        })
        .catch(err => {
          reject(err)
        })
      })
    },
    resendVerifyEmail({commit}, email){
      return new Promise((resolve, reject) => {
        $backend.$resendVerifyEmail(email).then(responseDate => {
          resolve(responseDate)
        })
        .catch(err => {
          reject(err)
        })
      })
    }

  }
});

