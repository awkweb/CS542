import Vue from 'vue'
import Vuex from 'vuex'
import { fetchDishes } from './api'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    dishes: []
  },
  
  actions: {
    FETCH_DISHES: ({ commit }) => {
      return fetchDishes().then(dishes => commit('SET_DISHES', dishes))
    }
  },    

  mutations: {
    SET_DISHES: (state, dishes) => {
      state.dishes = dishes
    }
  },

  getters: {
    dishes: state => {
      return state.dishes
    }
  }
})

export default store