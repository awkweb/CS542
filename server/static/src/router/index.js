import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import HomeView from '../views/HomeView.vue'
import OrderView from '../views/OrderView.vue'

export default new Router({
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/order', name: 'order', component: OrderView }
  ]
})