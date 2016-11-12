<template>
  <div id="order-view">
    <h1>Time to place an order</h1>
    <div v-for="customer in customers">
        <order-customer v-bind:customer="customer"></order-customer>
        <button v-on:click="removeCustomer(customer.number)">Remove Customer</button>
    </div>
    <button v-on:click="addCustomer">Add Customer</button>
    <button v-on:click="createOrder">Create Order</button>
  </div>
</template>

<script>
import OrderCustomer from '../components/OrderCustomer.vue'

export default {
  name: 'order',

  data () {
    return {
      customers: []
    }
  },

  components: {
    'order-customer': OrderCustomer
  },

  methods: {
    addCustomer: function () {
      var number = 0
      if (this.customers.length > 0) {
        var customerNumbers = this.customers.map(c => c.number)
        number = Math.max(...customerNumbers)
      }

      const customer = {
        'number': number + 1,
        'dishes': []
      };
      this.customers.push(customer);
    },

    removeCustomer: function (customerNumber) {
      this.customers = this.customers.filter(customer => customer.number != customerNumber
      )
    },

    createOrder: function () {
      // Create master order
      // For customer in customers, create order
      // Add dish to order
      // Navigate to home
    }
  },

  created () {
    this.$store.dispatch('FETCH_DISHES');
    this.addCustomer()
  }
}
</script>

<style lang="sass">

</style>
