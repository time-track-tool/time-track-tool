import Vue from "vue";
import Vuex from "vuex";
import api from "./modules/api";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    user_id: 9,
    debug: false,
    version: process.env.VERSION,
  },
  getters: {
    debug: (state) => {
      return state.debug;
    },
    user_id: (state) => {
      return state.user_id;
    },
  },
  mutations: {
    setDebug(state, debug) {
      state.debug = debug;
    },
    setUserId(state, user_id) {
      state.user_id = user_id;
    },
  },
  actions: {},
  modules: {
    rest: api,
  },
});
