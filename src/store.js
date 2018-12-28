import Vue from "vue";
import Vuex from "vuex";
import $backend from '@/backend';
Vue.prototype.$backend = $backend;

Vue.use(Vuex);

const clean = (data) => {
  Object.keys(data).forEach((key) => (data[key] == null) && delete data[key]);
}

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
    dorms:[],
    userFilters: {
      category: null,
      duration: null,
      dorm_features: [],
      room_features: [],
      additional_filters: []
    },
    reservationStepperState:{
      receiptUploaded: false,
      uploadNewReceipt: false,
      uploadDeadline: true,
      newAmount: false
    },
    managerDorms: [],
    reservation: {},
    manageReservation: [],
    manageDorm: {},
    authStatus: '',
    dormFeatures: [],
    isAuth: localStorage.getItem('auth'),
    isAdmin: localStorage.getItem('admin')
  },
  getters:{
    lang: state => {
      const currentLang = state.language
      const lang = require(`../locale/student.${currentLang}.json`);
      return lang[currentLang]
    },
    activeCurrency: state => state.currencySymbol,
    isLoggedIn: state => !!state.isAuth,
    isAdmin: state => !!state.isAdmin,
    authStatus: state => state.authStatus,
    reservationData: state => state.reservation,
    managerDorms: state => state.managerDorms,
    adminActiveComponent: state => state.adminActiveComponent,
    drawer: state => state.drawer,
    manageReservation: state => state.manageReservation,
    manageDorm: state => state.manageDorm,
    snackbar : state => state.snackbar,
    reservationStepperState: state => state.reservationStepperState
  },
  mutations: {
    updateSnackbar(state , payload){
      state.snackbar.trigger = true
      state.snackbar.message = payload.message
      state.snackbar.color = payload.color
    },
    fetchLocale(state){
      $backend.$fetchLocale().then(responseDate => {
        state.currencies = responseDate.currencies;
        state.languages = responseDate.languages;
        localStorage.setItem("lang", responseDate.languages[0].code);
        localStorage.setItem("currency-code", responseDate.currencies[0].code);
        localStorage.setItem("currency-symbol", responseDate.currencies[0].symbol);
      });
    },
    fetchFilters(state){
      $backend.$fetchFilters(state.language, state.currencyCode).then(responseDate => {
        state.filters = responseDate;
      });
    },
    fetchDorms(state) {
      $backend.$fetchDorms(state.language, state.currencyCode).then(responseDate => {
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
    reserveRoom(state, {room, responseDate}){
      localStorage.setItem("room", JSON.stringify({room}))
      localStorage.setItem('auth', JSON.stringify({
        user_name: responseDate.user.name,
        reservarion_id : responseDate.id,
        current_step: responseDate.user.current_step
      }))
    },
    fetchReservation(state, id){
      $backend.$fetchReservation(id).then(responseDate => {
        state.reservation = responseDate;
      });
    },
    fetchManagerDorms(state, responseDate){
      state.managerDorms = responseDate
    },
    fetchManagerReservation(state, responseDate){
      state.manageReservation = responseDate
    },
    fetchManagerDorm(state, responseDate){
      state.manageDorm = responseDate
      let selectFeaturesHolder = []
      for(const feature of responseDate.features){
        selectFeaturesHolder.push(feature.id)
      }
      state.dormFeatures = selectFeaturesHolder
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
    fetchSearchedDorms(context){
      context.commit('fetchSearchedDorms');
    },
    auth({commit}){
      return new Promise((resolve, reject) => {
        $backend.$auth().then(responseDate => {
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
      })
    },
    login({commit},user){
      return new Promise((resolve, reject) => {
        $backend.$login(user).then(responseDate => {
          resolve(responseDate)
        })
        .catch(err => {
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
    reserveRoom(context,room){

      return new Promise((resolve, reject) => {
        $backend.$reserveRoom(room.id).then(responseDate => {
          context.commit('reserveRoom', {room, responseDate})
          resolve(responseDate)
        })
        .catch(err => {
          reject(err)
        })
      });
      
    },
    fetchReservation(context, id){
      context.commit('fetchReservation', id)
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
    },
    resetPassword({commit}, email){
      return new Promise((resolve, reject) => {
        $backend.$resetPassword(email).then(responseDate => {
          resolve(responseDate)
        })
        .catch(err => {
          reject(err)
        })
      })
    },
    resetPasswordConfirm({commit}, data){
      return new Promise((resolve, reject) => {
        $backend.$resetPasswordConfirm(data).then(responseDate => {
          resolve(responseDate)
        })
        .catch(err => {
          reject(err)
        })
      })
    },
    uploadReceipt({commit}, data){
      return new Promise((resolve, reject) => {
        $backend.$uploadReceipt(data.id, data.formData).then(response => {
          resolve(response)
        })
        .catch(err => {
          reject(err)
        })
      })
    },
    uploadPhotos({commit}, data){
      return new Promise((resolve, reject) => {
        $backend.$uploadPhotos(data.id, data.formData).then(response => {
          resolve(response)
        })
        .catch(err => {
          reject(err)
        })
      })
    },
    upload360Photos({commit}, {dormId,data}){
      return new Promise((resolve, reject) => {
        $backend.$upload360Photos(dormId, data).then(response => {
          resolve(response)
        })
        .catch(err => {
          reject(err)
        })
      })
    },
    uploadDormCover({commit}, data){
      return new Promise((resolve, reject) => {
        $backend.$updateDormCover(data.id, data.formData).then(response => {
          resolve(response)
        })
        .catch(err => {
          reject(err)
        })
      })
    },
    fetchManagerDorms(context){
      return new Promise((resolve, reject) => {
        $backend.$fetchManagerDorms().then(response => {
          context.commit('fetchManagerDorms', response)
          resolve(response)
        }).catch(err => {
          reject(err)
        })
      })
    },
    fetchManagerReservation(context, id){
      return new Promise((resolve, reject) => {
        $backend.$fetchManagerReservation(id).then(response => {
          context.commit('fetchManagerReservation', response)
          resolve(response)
        }).catch(err => {
          reject(err)
        })
      })
    },
    fetchManagerDorm(context, id){
      return new Promise((resolve, reject) => {
        $backend.$fetchManagerDorm(id).then(response => {
          context.commit('fetchManagerDorm', response)
          resolve(response)
        }).catch(err => {
          reject(err)
        })
      })
    },
    updateReservationStatus(context, data){
      clean(data)
      return new Promise((resolve, reject) => {
        $backend.$updateReservationStatus(data).then(responseDate => {
          resolve(responseDate)
        })
        .catch(err => {
          reject(err)
        })
      })
    },
    updateDormInfo(context, data){
      clean(data)
      return new Promise((resolve, reject) => {
        $backend.$updateDormInfo(data).then(responseDate => {
          resolve(responseDate)
        })
        .catch(err => {
          reject(err)
        })
      })
    },
    addBankAccount(context, {id ,data}){
      return new Promise((resolve, reject) => {
        $backend.$addBankAccount(id,data).then(responseDate => {
          resolve(responseDate)
        })
        .catch(err => {
          reject(err)
        })
      })
    },
    deleteBankAccount(context, {dormId,accountId}){
      return new Promise((resolve, reject) => {
        $backend.$deleteBankAccount(dormId,accountId).then(responseDate => {
          resolve(responseDate)
        })
        .catch(err => {
          reject(err)
        })
      })
    },
    updateBankAccount(context, {dormId, accountId, data}){
      return new Promise((resolve, reject) => {
        $backend.$updateBankAccount(dormId,accountId,data).then(responseDate => {
          resolve(responseDate)
        })
        .catch(err => {
          reject(err)
        })
      })
    }


  }
});

