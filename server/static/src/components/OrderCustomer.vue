<template>
  <div>
    <div class="customer-header">
      <h3>Customer {{ customer.number }}</h3>
      <div>
        <button v-on:click="addDish" class="c-btn c-btn--secondary">Add Dish</button>
        <button v-on:click="removeCustomer" class="c-btn c-btn--secondary">Remove</button>
      </div>
    </div>
    <div v-for="dish in customer.dishes">
        <order-dish v-bind:dish="dish" v-on:removeDish="removeDish"></order-dish>
    </div>
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
    removeCustomer: function () {
      this.$emit('removeCustomer', this.customer.number)
    },

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

<style lang="sass">
.customer-header {
  display: flex;
  justify-content: space-between;
  height: 45px;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #EAEAEA;

  .c-btn {
    padding: 4px 10px;
    font-size: 12px;
  }
}
</style>