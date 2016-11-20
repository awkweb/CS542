import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import HomeView from '../views/HomeView.vue'
import OrderView from '../views/OrderView.vue'
import SplitView from '../views/SplitView.vue'
import BillView from '../views/BillView.vue'

export default new Router({
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/order/new', name: 'order-new', component: OrderView },
    { path: '/order/:id', name: 'order-update', component: OrderView },
    { path: '/split/:id', name: 'split', component: SplitView },
    { path: '/bill/:id', name: 'bill', component: BillView }
  ]
})