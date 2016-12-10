<template>
  <div id="split-view">
    <h2>Split</h2>

    <div class="wrapper">

      <div id="source">
        <div class="split-header">
          <h3>Customers</h3>
          <span class="bill-total">{{ bills[0].customers.length }} remaining</span>
        </div>
        <div id="container-0" class="container">
          <div v-bind:id="'customer-' + customer.id" v-for="customer in bills[0].customers" :key="customer.id">
            <div class="customer-number">Customer {{ customer.id }}</div>
            <div>${{ customer.dishes | total }}</div>
          </div>
        </div>
      </div>

      <div id="target">
        <div v-for="bill in bills.slice(1, bills.length)">
          <div class="split-header">
            <h3>Bill {{ bill.number }}</h3>
            <div>
              <span class="bill-total">${{ bill.total.toFixed(2) }}</span>
              <button v-on:click="removeBill(bill.number)" class="c-btn c-btn--secondary">Remove</button>
            </div>
          </div>
          <div v-bind:id="'container-' + bill.number" class="container">
            <div v-bind:id="'customer-' + customer.id" v-for="customer in bill.customers" :key="customer.id">
              <div class="customer-number">Customer {{ customer.id }}</div>
              <div>${{ customer.dishes | total }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="sticky-footer">
        <div>
          <button v-on:click="addBill" class="c-btn c-btn--secondary" v-bind:disabled="numberOfCustomers < bills.length">Add Bill</button>
          <button v-on:click="individualBills" class="c-btn c-btn--secondary" v-bind:disabled="numberOfCustomers != bills[0].customers.length">Individual Bills</button>
        </div>
        <div>
          <button v-on:click="back" class="c-btn c-btn--secondary">Back</button>
          <button v-on:click="splitOrders" class="c-btn c-btn--primary" v-bind:disabled="bills[0].customers.length > 0">{{ buttonText }}</button>
        </div>
      </div>
    </div>
</template>

<script>
import router from '../router'
import store from '../store'
import axios from 'axios'
import dragula from 'dragula'

export default {
  name: 'split',

  data () {
    return {
      drake: dragula(),
      numberOfCustomers: 0,
      bills: [
        { 'number': 0, 'customers': [], 'total': 0, 'dom_id': 'container-0' }
      ],
      buttonText: 'Finish'
    }
  },

  methods: {
    back: function () {
      const orderId = this.$route.params.id
      router.push({ name: 'order-update', params: { id: orderId } })
    },

    individualBills: function () {
      var cBill = this.bills[0]
      this.bills = [cBill]
      for (var i in cBill.customers) {
        const customer = cBill.customers[i]
        const total = parseFloat(this.customerTotal(customer.dishes))
        this.addBill()
        var lastBill = this.bills[this.bills.length - 1]
        lastBill.customers.push(customer)
        lastBill.total += total
        cBill.total -= total
      }
      cBill.customers = []
    },

    removeBill: function (billNumber) {
      const rBill = this.getBillWithNumber(billNumber)
      const billCustomers = rBill.customers
      var cBill = this.getBillWithNumber(0)
      cBill.customers = cBill.customers.concat(billCustomers)

      this.bills = this.bills.filter(bill => bill.number != billNumber
      )
    },

    getBillWithNumber: function (billNumber) {
      const bill = this.bills.filter(b => b.number == billNumber
      )[0]
      return bill
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
        'total': 0,
        'dom_id': 'container-' + (number + 1)
      }
      this.bills.push(bill)
      this.$nextTick(function () {
        const container = document.querySelector('#container-' + bill.number)
        this.drake.containers.push(container)
      })
    },

    splitOrders: function () {
      this.buttonText = 'Working...'
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
              if (i == vm.bills.length - 1 && x == bill.customers.length - 1) {
                axios.post('/api/masterorder/update/status', {
                  id: customer.master_order_id,
                  status: "Closed"
                })
                .then(function (response) {
                  console.log(response.data)
                  router.push({ name: 'home', query: { success: 1 }})                 
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
        const customers = response.data.orders.map(function (order) {
          return {
            'id': order.id,
            'dom_id': "customer-" + order.id,
            'master_order_id': order.master_order_id,
            'bill_id': order.bill_id,
            'dishes': order.order_dishes,
            'note': order.note
          }
        })
        vm.numberOfCustomers = customers.length
        vm.bills[0].customers = customers
        const container = document.querySelector('#container-0')
        vm.drake.containers.push(container)
        vm.addBill()
      })
      .catch(function (error) {
        console.log(error)
      })
    },

    getBillWithDomId: function (domId) {
      const bill = this.bills.filter(b => b.dom_id == domId
      )[0]
      return bill
    },

    getCustomerWithDomId: function (billDomId, customerDomId) {
      const bill = this.getBillWithDomId(billDomId)
      const customer = bill.customers.filter(c => c.dom_id == customerDomId
      )[0]
      return customer
    },

    customerTotal: function (orders) {
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
    
    var vm = this

    this.drake.on('drop', function(element, target, source, sibling) {
      var index = [].indexOf.call(element.parentNode.children, element)

      if (target.id != source.id) {
        var sourceBill = vm.getBillWithDomId(source.id)
        var targetBill = vm.getBillWithDomId(target.id)
        const customer = vm.getCustomerWithDomId(source.id, element.id)
        targetBill.customers.splice(index, 0, customer)
        sourceBill.customers = sourceBill.customers.filter(c => c.id != customer.id)
        const total = parseFloat(vm.customerTotal(customer.dishes))
        sourceBill.total -= total
        targetBill.total += total
      }
    })
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

  &>div {
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

.gu-mirror {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #007ee5;
  background: #fff;
  transition: opacity 0.4s ease-in-out;
  border: 1px solid #D0D4D9;
  border-radius: 4px;
  cursor: move;
  cursor: grab;
  cursor: -moz-grab;
  cursor: -webkit-grab;

  div {
    font-weight: 500;
    padding: 0 1rem;
  }
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
