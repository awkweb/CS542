<template>
  <div>
    <h3>Customer {{ customer.number }}</h3>
    <div v-for="dish in customer.dishes">
        <order-dish v-bind:dish="dish"></order-dish>
        <button v-on:click="removeDish(dish.number)">Remove Dish</button>
    </div>
    <button v-on:click="addDish">Add Dish</button>
  </div>
</template>

<script>
import OrderDish from '../components/OrderDish.vue'

export default {
  name: 'customerOrder',

  props: ['customer'],

  components: {
    'order-dish': OrderDish
  },

  methods: {
    addDish: function () {
      var number = 0
      if (this.customer.dishes.length > 0) {
        var dishNumbers = this.customer.dishes.map(c => c.number)
        number = Math.max(...dishNumbers)
      }

      const dish = {
        'number': number + 1,
        'id': -1,
        'quantity': 0
      };
      this.customer.dishes.push(dish)
    },

    removeDish: function (dishNumber) {
      this.customer.dishes = this.customer.dishes.filter(dish => dish.number != dishNumber)
    }
  }
}
</script>
