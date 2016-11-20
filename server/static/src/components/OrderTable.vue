<template>
  <table class="c-table">
    <thead>
      <th>Order #</th>
      <th>Date</th>
      <th>Customers</th>
      <th>Total</th>
      <th>Status</th>
    </thead>
    <tbody v-for="order in orders">
      <tr v-if="order.status == orderFilter || orderFilter == 'All'" v-on:click="handleClick(order)">
        <td>{{ order.id }}</td>
        <td>{{ order.date | prettyDate }}</td>
        <td>{{ order.orders.length }}</td>
        <td>${{ order.orders | total }}</td>
        <td>{{ order.status }}</td>
      </tr>
    </tbody>  
  </table>
</template>

<script>
import router from '../router'
import store from '../store'
import moment from 'moment'

export default {
  name: 'homeTable',
  
  props: ['orders', 'orderFilter'],

  methods: {
    handleClick: function (order) {
      console.log(order)
      const orderId = order.id
      const orderStatus = order.status
      if (orderStatus === 'Open')
        router.push({ name: 'order-update', params: { id: orderId }})
      else
        router.push({ name: 'bill', params: { id: orderId }})
    }
  },
  
  filters: {
    total: function (orders) {
      var orderDict = {}
      for (var i in orders) {
        const order = orders[i]
        const dishes = order.order_dishes
        for (var n in dishes) {
          const dish = dishes[n]
          const dishId = parseInt(dish.dish_id)

          if (orderDict[dishId]) {
            orderDict[dishId] += dish.quantity
          } else {
            orderDict[dishId] = dish.quantity
          }
        }
      }

      const dishes = store.state.dishes
      var sum = 0
      for (var dishId in orderDict) {
        const quantity = orderDict[dishId]
        const dish = dishes.filter(d => d.id == dishId)[0]
        sum += dish.price * quantity
      }

      return sum.toFixed(2)
    },

    prettyDate: function (dateString) {
      return moment(dateString).format('MMMM D, YYYY')
    }
  }
}
</script>

<style lang="sass">
table {
  margin-bottom: 23px;
}

table {
  border-collapse: collapse;
}

.c-table {
  display: table;
  width: 100%;
  text-align: left;

  tr:hover {
    background: #f7f9fa;
    cursor: pointer;
  }
}

.c-table__th, .c-table th, .c-table__td, .c-table td {
  padding-top: 11.5px;
  padding-bottom: 11.5px;
  padding-left: 5.75px;
  padding-right: 5.75px;
}

.c-table__th, .c-table th {
  font-weight: 600;
  color: #737373;
  border-bottom: 2px solid #d0d4d9;
}

.c-table__row, .c-table tr {
  border-bottom: 1px solid #d0d4d9;
}
</style>
