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
    adminActiveComponent: null,
    snackbar: {
      trigger: false,
      message: '',
      color: ''
    },
    currencies: [],
    languages: [],
    filters: [],
    dorms: [],
    userFilters: {
      category: null,
      duration: null,
      dorm_features: [],
      room_features: [],
      additional_filters: []
    },
    reservationStepperState: {
      receiptUploaded: false,
      uploadNewReceipt: false,
      uploadDeadline: true,
      newAmount: false
    },
    managerDorms: [],
    managerDormRooms: [],
    reservation: {},
    manageReservation: [],
    manageDorm: {},
    authStatus: '',
    dormFeatures: [],
    isAuth: localStorage.getItem('auth'),
    isAdmin: localStorage.getItem('admin')
  },
  getters: {
    lang: state => {
      const currentLang = state.language
      const lang = require(`../../locale/${currentLang}.json`);
      return lang[currentLang]
    },
    activeCurrency: state => state.currencySymbol,
    isLoggedIn: state => !!state.isAuth,
    isAdmin: state => !!state.isAdmin,
    authStatus: state => state.authStatus,
    reservationData: state => state.reservation,
    managerDorms: state => state.managerDorms,
    managerDormRooms: state => state.managerDormRooms,
    adminActiveComponent: state => state.adminActiveComponent,
    drawer: state => state.drawer,
    manageReservation: state => state.manageReservation,
    manageDorm: state => state.manageDorm,
    snackbar: state => state.snackbar,
    reservationStepperState: state => state.reservationStepperState
  },
  mutations: {
    updateSnackbar(state, payload) {
      state.snackbar.trigger = true
      state.snackbar.message = payload.message
      state.snackbar.color = payload.color
    },
    fetchLocale(state, responseDate) {
      state.currencies = responseDate.currencies;
      state.languages = responseDate.languages;
      localStorage.setItem("currency-code", responseDate.currencies[0].code);
      localStorage.setItem("currency-symbol", responseDate.currencies[0].symbol);
    },
    fetchFilters(state, responseDate) {
      state.filters = responseDate;
    },
    fetchDorms(state) {
      $backend.$fetchDorms(state.currencyCode).then(responseDate => {
        state.dorms = responseDate;
      });
    },
    fetchSearchedDorms(state) {
      let filters = {
        lang: state.language,
        currency: state.currencyCode,
        duration: state.userFilters.duration,
        category: state.userFilters.category,
        dormFeatures: state.userFilters.dorm_features,
        roomFeatures: state.userFilters.room_features,
        additionalFilters: state.userFilters.additional_filters
      }
      $backend.$searchDorms(filters).then(responseDate => {
        state.dorms = responseDate;
      });
    },
    auth_success(state) {
      state.authStatus = 'Success'
      state.isAuth = !!localStorage.getItem('auth')
      state.isAdmin = localStorage.getItem('admin')
    },
    auth_error(state) {
      state.authStatus = 'An error occur'
    },
    logout(state) {
      state.isAuth = null
      state.isAdmin = null
    },
    registerSuccess(state) {
      state.authStatus = 'Registeration Faild'
    },
    reserveRoom(state, { room, responseDate }) {
      localStorage.setItem("room", JSON.stringify({ room }))
      localStorage.setItem('auth', JSON.stringify({
        user_name: responseDate.user.name,
        reservarion_id: responseDate.id,
        current_step: responseDate.user.current_step
      }))
    },
    fetchReservation(state, responseDate) {
      state.reservation = responseDate;
    },
    fetchManagerDorms(state, responseDate) {
      state.managerDorms = responseDate
    },
    fetchManagerDormRooms(state, responseDate) {
      state.managerDormRooms = responseDate
    },
    fetchManagerReservation(state, responseDate) {
      state.manageReservation = responseDate
    },
    fetchManagerDorm(state, responseDate) {
      state.manageDorm = responseDate
      let selectFeaturesHolder = []
      for (const feature of responseDate.features) {
        selectFeaturesHolder.push(feature.id)
      }
      state.dormFeatures = selectFeaturesHolder
    }
  },
  actions: {
    fetchLocale({ commit }) {
      $backend.$fetchLocale().then(responseDate => {
        commit('fetchLocale', responseDate);
      });
    },
    fetchFilters({ commit }, currentCurrency) {
      return new Promise((resolve, reject) => {
        $backend.$fetchFilters(currentCurrency).then(responseDate => {
          commit('fetchFilters', responseDate);
          resolve(responseDate)
        })
          .catch(err => {
            reject(err)
          })
      })
    },
    fetchDorms({ commit }) {
      commit('fetchDorms');
    },
    fetchSearchedDorms({ commit }) {
      commit('fetchSearchedDorms');
    },
    auth({ commit }) {
      return new Promise((resolve, reject) => {
        $backend.$auth().then(responseDate => {
          if (responseDate.is_manager) {
            localStorage.setItem('admin', true)
          }
          localStorage.setItem('auth', JSON.stringify({
            user_name: responseDate.name,
            reservarion_id: responseDate.reservation_id,
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
      })
    },
    logout({ commit }) {
      return new Promise((resolve) => {
        commit('logout')
        localStorage.removeItem('auth')
        localStorage.removeItem('admin')
        resolve()
      });
    },
    reserveRoom({ commit }, room) {
      return new Promise((resolve, reject) => {
        $backend.$reserveRoom(room.id).then(responseDate => {
          commit('reserveRoom', { room, responseDate })
          resolve(responseDate)
        })
          .catch(err => {
            reject(err)
          })
      });
    },
    fetchReservation({ commit }, id) {
      $backend.$fetchReservation(id).then(responseDate => {
        commit('fetchReservation', responseDate)
      });
    },
    register({ commit }, user) {
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
    fetchManagerDorms({ commit }) {
      return new Promise((resolve, reject) => {
        $backend.$fetchManagerDorms().then(response => {
          commit('fetchManagerDorms', response)
          resolve(response)
        }).catch(err => {
          reject(err)
        })
      })
    },
    fetchManagerReservation({ commit }, id) {
      return new Promise((resolve, reject) => {
        $backend.$fetchManagerReservation(id).then(response => {
          commit('fetchManagerReservation', response)
          resolve(response)
        }).catch(err => {
          reject(err)
        })
      })
    },
    fetchManagerDorm({ commit }, id) {
      return new Promise((resolve, reject) => {
        $backend.$fetchManagerDorm(id).then(response => {
          commit('fetchManagerDorm', response)
          resolve(response)
        }).catch(err => {
          reject(err)
        })
      })
    },
    fetchManagerDormRooms({ commit }, id) {
      return new Promise((resolve, reject) => {
        $backend.$fetchManagerDormRooms(id).then(response => {
          commit('fetchManagerDormRooms', response)
          resolve(response)
        }).catch(err => {
          reject(err)
        })
      })
    }
  }
});

