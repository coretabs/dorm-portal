import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    language: localStorage.getItem("lang") || 'en'
  },
  getters:{
    lang: state => {
      let currentLang = state.language
      const lang = require(`../locale/student.${currentLang}.json`);
      return lang[currentLang]
    }
  },
  mutations: {
  },
  actions: {}
});

