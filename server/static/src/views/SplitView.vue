<template>
  <div id="split-view">
    <h2>Split</h2>

    <div class="wrapper">
      <div id="source">
        <div class="split-header">
          <h3>Customers</h3>
          <span class="bill-total">{{ customers.length }} remaining</span>
        </div>
        <div class="container" v-dragula="customers" bag="first-bag">
          <div v-for="customer in customers" :key="customer.id">
            <span class="customer-number">Customer {{ customer.number }}</span>
            <span>${{ customer.dishes | total }}</span>
          </div>
        </div>
      </div>
      <div id="target">
        <div v-for="bill in bills">
          <div class="split-header">
            <h3>Bill {{ bill.number }}</h3>
            <div>
              <span class="bill-total">${{ bill.total.toFixed(2) }}</span>
              <button v-on:click="removeBill(bill.number)" class="c-btn c-btn--secondary">Remove</button>
            </div>
          </div>
          <div class="container" v-dragula="bill.customers" bag="first-bag">
            <div v-for="customer in bill.customers" :key="customer.id">
              <span class="customer-number">Customer {{ customer.number }}</span>
              <span>${{ customer.dishes | total }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="sticky-footer">
      <button v-on:click="addBill" class="c-btn c-btn--secondary" v-if="numberOfCustomers <= bills.length" disabled>Add Bill</button>
      <button v-on:click="addBill" class="c-btn c-btn--secondary" v-else>Add Bill</button>
      <div>
        <button v-on:click="back" class="c-btn c-btn--secondary">Back</button>
        <button v-on:click="splitOrders" class="c-btn c-btn--primary" v-if="customers.length > 0" disabled>Finish</button>
        <button v-on:click="splitOrders" class="c-btn c-btn--primary" v-else>Finish</button>
      </div>
    </div>
  </div>
</template>

<script>
import router from '../router'
import store from '../store'
import Vue from 'vue'
import VueDragula from 'vue-dragula'
import axios from 'axios'

Vue.use(VueDragula);

export default {
  name: 'split',

  data () {
    return {
      numberOfCustomers: 0,
      customers: [],
      bills: [
        { 'number': 1, 'customers': [], 'total': 0 }
      ]
    }
  },

  methods: {
    back: function () {
      const orderId = this.$route.params.id
      router.push({ name: 'order-update', params: { id: orderId } })
    },

    removeBill: function (billNumber) {
      const rBill = this.bills.filter(b => b.number == billNumber
      )[0]
      const billCustomers = rBill.customers
      this.customers = this.customers.concat(billCustomers)

      this.bills = this.bills.filter(bill => bill.number != billNumber
      )
    },

    addBill: function () {
      var number = 0
      if (this.bills.length > 0) {
        var billNumbers = this.bills.map(b => b.number)
        number = Math.max(...billNumbers)
      }

      const bill = {
        'number': number + 1,
        'customers': [],
        'total': 0 
      }
      this.bills.push(bill)
    },

    splitOrders: function () {
      const vm = this
      const bills = vm.bills

      for (var i in bills) {
        const bill = bills[i]
        axios.post('/api/bill/add')
        .then(function (response) {
          const billId = response.data.id

          for (var x in bill.customers) {
            const customer = bill.customers[x]
            axios.post('/api/order/bill', {
                order_id: customer.id,
                bill_id: billId
            })
            .then(function (response) {
              console.log(response.data)
              if (i == vm.bills.length - 1 && x == bill.customers.length - 1) {
                axios.post('/api/masterorder/update/status', {
                  id: customer.master_order_id,
                  status: "Closed"
                })
                .then(function (response) {
                  console.log(response.data)
                  router.push({ name: 'home' })                  
                })
                .catch(function (error) {
                  console.log(error)
                }) 
              }
            })
            .catch(function (error) {
              console.log(error)
            }) 
          }
        })
        .catch(function (error) {
          console.log(error)
        })
      }
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
        vm.numberOfCustomers = vm.customers.length
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },

  filters: {
    total: function (orders) {
      var orderDict = {}
      for (var n in orders) {
        const dish = orders[n]
        const dishId = parseInt(dish.dish_id)

        if (orderDict[dishId]) {
          orderDict[dishId] += dish.quantity
        } else {
          orderDict[dishId] = dish.quantity
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
    }
  },

  watch: {
      '$route': 'getOrder'
  },

  created () {
    if (this.$route.params.id)
      this.getOrder()
  }
}
</script>

<style lang="sass">
.split-header {
  display: flex;
  justify-content: space-between;
  height: 45px;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #EAEAEA;

  .c-btn {
    padding: 5px 10px;
    font-size: 12px;
  }

  div {
    display: flex;
    align-items: center;
  }

  .bill-total {
    padding-right: 10px;
  }
}

.wrapper {
  display: flex;
  margin-bottom: 8rem;
}

#source , #target {
  flex: 1;
}

#source {
  padding-right: .5rem;
}

#target {
  padding-left: .5rem;
}

.container {
  min-height: 4rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #F7F9FA;
  border-radius: 4px;

  div {
    display: flex;
    justify-content: space-between;
    background: #fff;
    border: 1px solid #D0D4D9;
    border-radius: 4px;
    padding: 1rem;
    cursor: move;
    cursor: grab;
    cursor: -moz-grab;
    cursor: -webkit-grab;
    margin-bottom: 10px;

    .customer-number {
      font-weight: 500;
    }

    &:hover {
      background: linear-gradient(white, #f7f9fa);
    }

    &:last-child {
      margin-bottom: 0;
    }
  }
}

.container .scale-transition {
  overflow: hidden;
  transition: height .2s;
}

.container .scale-enter {
  height: 0px;
}

.container .scale-leave {
  height: 0px;
}

.gu-mirror {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
  background: #fff;
  transition: opacity 0.4s ease-in-out;
  border: 1px solid #D0D4D9;
  border-radius: 4px;
  cursor: move;
  cursor: grab;
  cursor: -moz-grab;
  cursor: -webkit-grab;
}

.gu-mirror {
  position: fixed !important;
  margin: 0 !important;
  z-index: 9999 !important;
  opacity: 0.8;
  -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=80)";
  filter: alpha(opacity=80);
}

.gu-hide {
  display: none !important;
}

.gu-unselectable {
  -webkit-user-select: none !important;
  -moz-user-select: none !important;
  -ms-user-select: none !important;
  user-select: none !important;
}

.gu-transit {
  opacity: 0.2;
  -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=20)";
  filter: alpha(opacity=20);
}

</style>
