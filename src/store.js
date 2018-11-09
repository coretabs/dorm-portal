import Vue from "vue";
import Vuex from "vuex";
import * as lang from './language'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    language: lang.language,
    cureentLang: 'en'
  },
  mutations: {},
  actions: {}
});
