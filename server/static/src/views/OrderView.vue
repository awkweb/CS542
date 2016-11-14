<template>
  <div id="order-view">
    <h2>New Order</h2>
    <div class="customer-container">
      <div v-for="customer in customers">
        <order-customer v-bind:customer="customer" v-on:removeCustomer="removeCustomer"></order-customer>
      </div>
    </div>

    <div class="sticky-footer">
      <button v-on:click="addCustomer" class="c-btn c-btn--secondary">Add Customer</button>
      <div>
        <button class="c-btn c-btn--secondary">Cancel</button>
        <button v-on:click="createOrder" class="c-btn c-btn--primary" disabled>Submit</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import OrderCustomer from '../components/OrderCustomer.vue'

export default {
  name: 'order',

  data () {
    return {
      customers: [],
      total: 0
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
      var vm = this;

      // axios.post('/api/masterorder/add')
      // .then(function (response) {
      //   const masterOrderId = response.data.id
      //   console.log("masterOrderId", masterOrderId);
      // })
      // .catch(function (error) {
      //   console.log(error);
      // });
    },
  },

  created () {
    this.$store.dispatch('FETCH_DISHES');
    this.addCustomer()
  }
}
</script>

<style lang="sass">
.customer-container {
  margin-bottom: 10rem;
}

.sticky-footer {
  display: flex;
  justify-content: space-between;
  position: fixed;
  max-width: 45rem;
  margin: auto;
  bottom: 0;
  right: 0;
  left: 0;
  padding: .5rem .5rem;
  border-top: 1px solid #EAEAEA;
  background: #fff;
}
</style>
