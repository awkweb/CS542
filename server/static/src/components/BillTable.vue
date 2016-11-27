<template>
  <table class="c-table bill-table">
    <thead>
      <th>Dish</th>
      <th class="align-number">Price</th>
      <th class="align-number">Quantity</th>
      <th class="align-number">Total</th>
    </thead>
    <tbody>
      <tr v-for="order in fOrders">
        <td>{{ order.name }}</td>
        <td class="align-number">${{ order.price }}</td>
        <td class="align-number">{{ order.quantity }}</td>
        <td class="align-number">${{ order.total }}</td>
      </tr>
      <tr class="grand-total">
        <td>Grand Total</td>
        <td></td>
        <td></td>
        <td class="align-number">${{ grandTotal }}</td>
      </tr>
    </tbody> 
  </table>
</template>

<script>
import store from '../store'

export default {
  name: 'billTable',
  
  props: ['orders'],

  computed: {
    fOrders: function () {
      var orderDict = {}
      for (var i in this.orders) {
        const order = this.orders[i]
        const dishes = order.order_dishes
        for (var n in dishes) {
          const dish = dishes[n]
          const dishId = parseInt(dish.dish_id)

          if (orderDict[dishId]) {
            orderDict[dishId]['quantity'] += dish.quantity
          } else {
            orderDict[dishId] = {}
            orderDict[dishId]['quantity'] = dish.quantity
          }
        }
      }

      const dishes = store.state.dishes
      var formattedOrders = []
      for (var dishId in orderDict) {
        const dish = dishes.filter(d => d.id == dishId)[0]
        const quantity = orderDict[dishId]['quantity']
        orderDict[dishId]['name'] = dish.name
        orderDict[dishId]['price'] = dish.price.toFixed(2)
        orderDict[dishId]['total'] = (dish.price * quantity).toFixed(2)
        formattedOrders.push(orderDict[dishId])
      }

      return formattedOrders
    },

    grandTotal: function () {
      var orderDict = {}
      for (var i in this.orders) {
        const order = this.orders[i]
        const dishes = order.order_dishes
        for (var n in dishes) {
          const dish = dishes[n]
          const dishId = parseInt(dish.dish_id)

          if (orderDict[dishId]) {
            orderDict[dishId]['quantity'] += dish.quantity
          } else {
            orderDict[dishId] = {}
            orderDict[dishId]['quantity'] = dish.quantity
          }
        }
      }

      const dishes = store.state.dishes
      var sum = 0
      for (var dishId in orderDict) {
        const dish = dishes.filter(d => d.id == dishId)[0]
        const quantity = orderDict[dishId]['quantity']
        sum += dish.price * quantity
      }

      return sum.toFixed(2)
    }
  }
}
</script>

<style lang="sass">
.bill-table {
  tbody>tr:nth-last-child(2) {
    border-bottom-width: 2px;
  }
}

.align-number {
  text-align: right;
}

.grand-total {
  font-weight: 500;
  border-bottom-width: 0 !important;

  &:hover {
    background: #fff !important;
  }
}
</style>
