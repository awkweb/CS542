<template>
  <div id="order-view">
    <h2>{{ titleText }}</h2>

    <div class="customer-container">
      <div v-for="customer in customers">
        <order-customer
          v-bind:customer="customer"
          v-on:removeCustomer="removeCustomer"
          v-on:removeDish="removeDish"
          v-on:changeDish="changeDish"
        ></order-customer>
      </div>
    </div>

    <div class="sticky-footer">
      <button v-on:click="addCustomer" class="c-btn c-btn--secondary">Add Customer</button>
      <div>
        <button v-on:click="cancel" class="c-btn c-btn--secondary">Cancel</button>
        <button v-on:click="split" class="c-btn c-btn--secondary" v-if="this.$route.params.id">Split</button>
        <button v-on:click="updateOrder" class="c-btn c-btn--primary" v-if="this.$route.params.id" v-bind:disabled="readyForSubmit">{{ buttonText }}</button>
        <button v-on:click="createOrder" class="c-btn c-btn--primary" v-bind:disabled="readyForSubmit" v-else>{{ buttonText }}</button>
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
      masterOrderId: -1,
      customers: [],
      titleText: 'New Order',
      buttonText: 'Submit',
      removeIds: {
        customerIds: [],
        dishIds: []
      },
      addCustomers: [],
      addDishes: [],
      updateDishes: []
    }
  },

  computed: {
    readyForSubmit: function () {
      return (this.customers.length == 0)
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

      const dish = {
        'number': number + 1,
        'dish_id': -1,
        'quantity': 1
      }
      customer.dishes.push(dish)
      this.customers.push(customer)
      this.addCustomers.push(customer)
    },

    removeCustomer: function (customer) {
      if (customer.id) {
        this.removeIds.customerIds.push(customer.id)
      }
      this.customers = this.customers.filter(c => c.number != customer.number)
    },

    changeDish: function (customerId, dish) {
      if (!this.removeIds.customerIds.includes(customerId) && dish.dish_id != -1) {
        if (dish.id) {
          this.updateDishes = this.updateDishes.filter(d => d.id != dish.id)
          this.updateDishes.push({
            'id': dish.id,
            'dishId': dish.dish_id,
            'quantity': dish.quantity
          })
        } else {
          this.addDishes = this.addDishes.filter(d => d.number != dish.number)
          this.addDishes.push({
            'orderId': customerId,
            'dishId': dish.dish_id,
            'quantity': dish.quantity,
            'number': dish.number
          })
        }
      }
    },

    removeDish: function (dish) {
      if (dish.id) {
        this.removeIds.dishIds.push(dish.id)        
        this.updateDishes = this.updateDishes.filter(d => d.id != dish.id)
      } else {
        this.addDishes = this.addDishes.filter(d => d.number != dish.number)
      }
    },

    deleteCustomerRequest: function (customerId) {
      return axios.delete('/api/order/delete', {
        params: {
          id: customerId
        }
      })
    },

    deleteDishRequest: function (dishId) {
      return axios.delete('/api/orderdish/delete', {
        params: {
          id: dishId
        }
      })
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
        vm.masterOrderId = response.data.id
        vm.customers = response.data.orders.map(function (order) {
          const order_dishes = order.order_dishes.map(function (od) {
            return {
              'number': od.id,
              'id': od.id,
              'dish_id': od.dish_id,
              'order_id': od.order_id,
              'quantity': od.quantity
            }
          })
          return {
            'number': order.id,
            'id': order.id,
            'master_order_id': order.master_order_id,
            'bill_id': order.bill_id,
            'dishes': order_dishes,
            'note': order.note
          }
        })
      })
      .catch(function (error) {
        console.log(error);
      })
    },

    createOrder: function () {
      this.buttonText = 'Working...'
      var vm = this

      axios.post('/api/masterorder/add')
      .then(function (response) {
        const masterOrderId = response.data.id

        for (var i in vm.customers) {
          const customer = vm.customers[i]

          vm.postOrderRequest(masterOrderId)
          .then(function (response) {
            const orderId = response.data.id

            for (var x in customer.dishes) {
              const dish = customer.dishes[x]
              axios.post('/api/orderdish/add', {
                order_id: orderId,
                dish_id: dish.dish_id,
                quantity: dish.quantity
              })
              .then(function (response) {
                if (i == vm.customers.length - 1 && x == customer.dishes.length - 1) {
                  router.push({ name: 'home', query: { success: 1 }})
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

    postOrderRequest: function (masterOrderId) {
      return axios.post('/api/order/add', {
        master_order_id: masterOrderId,
        note: ''
      })
    },

    postOrderDishRequest: function (orderId, dishId, quantity) {
      return axios.post('/api/orderdish/add', {
        order_id: orderId,
        dish_id: dishId,
        quantity: quantity
      })
    },

    addCustomerRequest: function (customer) {
      var vm = this
      this.postOrderRequest(this.masterOrderId)
      .then(function (response) {
        const orderId = response.data.id

        const dishRequests = customer.dishes.map(dish => vm.postOrderDishRequest(orderId, dish.dish_id, dish.quantity))
        axios.all(dishRequests)
        .then(function (response) {
          console.log(response)
        })
        .catch(function (error) {
          console.log(error)
        })
      })
      .catch(function (error) {
        console.log(error);
      })
    },

    updateOrderDishRequest: function (id, dishId, quantity) {
      return axios.post('/api/orderdish/update', {
        id: id,
        dish_id: dishId,
        quantity: quantity
      })
    },

    updateOrder: function () {
      var vm = this
      this.buttonText = 'Working...'
      
      var deleteRequests = []
      deleteRequests = deleteRequests.concat(this.removeIds.dishIds.map(id => this.deleteDishRequest(id)))
      deleteRequests = deleteRequests.concat(this.removeIds.customerIds.map(id => this.deleteCustomerRequest(id)))

      var changeRequests = []
      changeRequests = changeRequests.concat(this.updateDishes.map(dish => this.updateOrderDishRequest(dish.id, dish.dishId, dish.quantity)))
      changeRequests = changeRequests.concat(this.addDishes.map(dish => this.postOrderDishRequest(dish.orderId, dish.dishId, dish.quantity)))

      axios.all(deleteRequests)
      .then(function (response) {
        axios.all(changeRequests)
        .then(function (response) {
          if (vm.addCustomers.length > 0) {
            for (var i in vm.addCustomers) {
              const customer = vm.addCustomers[i]
              vm.addCustomerRequest(customer)

              if (i == vm.addCustomers.length - 1) {
                router.push({ name: 'home', query: { success: 1 }})
              }
            }
          } else {
            router.push({ name: 'home', query: { success: 1 }})
          }
        })
        .catch(function (error) {
          console.log(error)
        })
      })
      .catch(function (error) {
        console.log(error)
      })      
    }
  },

  watch: {
    '$route': 'getOrder'
  },

  created () {
    if (this.$route.params.id) {
      this.titleText = 'Update Order #' + this.$route.params.id
      this.buttonText = 'Update'
      this.getOrder()
    }
    else {
      this.buttonText = 'Submit'
      this.addCustomer()
    }
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
