<template>
  <div id="order-view">
    <h2 v-if="this.$route.params.id">Update Order #{{ this.$route.params.id }}</h2>
    <h2 v-else>New Order</h2>

    <div class="customer-container">
      <div v-for="customer in customers">
        <order-customer v-bind:customer="customer" v-on:removeCustomer="removeCustomer"></order-customer>
      </div>
    </div>

    <div class="sticky-footer">
      <button v-on:click="addCustomer" class="c-btn c-btn--secondary">Add Customer</button>
      <div>
        <button v-on:click="cancel" class="c-btn c-btn--secondary">Cancel</button>
        <button v-on:click="split" class="c-btn c-btn--secondary" v-if="this.$route.params.id">Split</button>
        <button v-on:click="updateOrder" class="c-btn c-btn--primary" v-if="this.$route.params.id">Update</button>
        <button v-on:click="createOrder" class="c-btn c-btn--primary" v-else>Submit</button>
      </div>
    </div>
  </div>
</template>

<script>
import router from '../router'
import axios from 'axios'
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
    cancel: function () {
      router.push({ name: 'home' })
    },

    split: function () {
      const orderId = this.$route.params.id
      router.push({ name: 'split', params: { id: orderId } })
    },

    addCustomer: function () {
      var number = 0
      if (this.customers.length > 0) {
        var customerNumbers = this.customers.map(c => c.number)
        number = Math.max(...customerNumbers)
      }

      const customer = {
        'number': number + 1,
        'dishes': []
      }
      this.customers.push(customer)
    },

    removeCustomer: function (customerNumber) {
      this.customers = this.customers.filter(customer => customer.number != customerNumber
      )
    },

    getOrder: function () {
      var vm = this
      const orderId = this.$route.params.id

      axios.get('/api/masterorder', {
        params: {
          id: orderId
        }
      })
      .then(function (response) {
        vm.customers = response.data.orders.map(function (order) {
          return {
            'number': order.id,
            'id': order.id,
            'master_order_id': order.master_order_id,
            'bill_id': order.bill_id,
            'dishes': order.order_dishes,
            'note': order.note
          }
        })
      })
      .catch(function (error) {
        console.log(error);
      })
    },

    createOrder: function () {
      var vm = this

      axios.post('/api/masterorder/add')
      .then(function (response) {
        const masterOrderId = response.data.id
        console.log("Master Order Id: " + masterOrderId + "\n======================")

        for (var i in vm.customers) {
          const customer = vm.customers[i]

          axios.post('/api/order/add', {
            master_order_id: masterOrderId,
            note: ''
          })
          .then(function (response) {
            const orderId = response.data.id
            console.log("Order Id: " + orderId + "\n======================")

            for (var x in customer.dishes) {
              const dish = customer.dishes[x]
              axios.post('/api/orderdish/add', {
                order_id: orderId,
                dish_id: dish.dish_id,
                quantity: dish.quantity
              })
              .then(function (response) {
                console.log(response.data)
                if (i == vm.customers.length - 1 && x == customer.dishes.length - 1) {
                  router.push({ name: 'home' })
                }
              })
              .catch(function (error) {
                console.log(error);
              })
            } 
          })
          .catch(function (error) {
            console.log(error);
          })
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },

    updateOrder: function () {
      var vm = this
      console.log(vm.customers)

      // add, delete customer
      // create, update, delete dish
      // keep track of orders in store.js
    }
  },

  watch: {
    '$route': 'getOrder'
  },

  created () {
    if (this.$route.params.id)
      this.getOrder()
    else
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
  padding: .5rem 0;
  border-top: 1px solid #EAEAEA;
  background: #fff;
}
</style>
