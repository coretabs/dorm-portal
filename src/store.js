import Vue from "vue";
import Vuex from "vuex";
import $backend from '@/backend';
Vue.prototype.$backend = $backend;

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    language: localStorage.getItem("lang"),
    currency: localStorage.getItem("currency"),
    drawer: null,
    reservationStep: 1,
    currencies: [],
    languages: [],
    filters: [],
    dorms:[]
  },
  getters:{
    lang: state => {
      const currentLang = state.language
      const lang = require(`../locale/student.${currentLang}.json`);
      return lang[currentLang]
    },
    activeCurrency: state => {
      return state.currency
    },
  },
  mutations: {
    fetchFilters(state){
      $backend.$fetchFilters().then(responseDate => {
        state.filters = responseDate;
      });
    },
    fetchDorms(state) {
      $backend.$fetchDorms().then(responseDate => {
        state.dorms = responseDate;
      });
    }
  },
  actions: {
    fetchFilters(context){
      context.commit('fetchFilters');
    },
    fetchDorms(context) {
      context.commit('fetchDorms');
    }
  }
});

