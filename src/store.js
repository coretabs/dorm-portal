import Vue from "vue";
import Vuex from "vuex";
import language from '../locale/student.en.json'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    language: language
  },
  mutations: {},
  actions: {}
});
