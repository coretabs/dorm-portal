import Vue from "vue";
import Vuex from "vuex";
import $backend from '@/backend';
Vue.prototype.$backend = $backend;
import actions from './actions'
import mutations from './mutations'
import getters from './getters'
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
  getters,
  mutations,
  actions
});

