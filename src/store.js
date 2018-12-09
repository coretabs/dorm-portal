import Vue from "vue";
import Vuex from "vuex";
import $backend from '@/backend';
Vue.prototype.$backend = $backend;

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    language: localStorage.getItem("lang") || "en",
    currencyCode: localStorage.getItem("currency-code") || "USD",
    currencySymbol: localStorage.getItem("currency-symbol") || "$",
    drawer: null,
    reservationStep: 1,
    currencies: [],
    languages: [],
    filters: [],
    dorms:[],
    user:{}
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
        console.log(responseDate)
      });
    },
    fetchDorms(state) {
      $backend.$fetchDorms().then(responseDate => {
        state.dorms = responseDate;
      });
    },
    login(state){
      $backend.$login().then(responseDate => {
        if(responseDate.status == 200){
          //localStorage.setItem("user", JSON.stringify({responseDate}));
        }
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
    login(context) {
      context.commit('login');
    }
  }
});

