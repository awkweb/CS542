<template>
  <div id="split-view">
    <h2>Split</h2>

    <div class="wrapper">
      <div id="source">
        <div class="split-header">
          <h3>{{ customers.length }} Customers</h3>
        </div>
        <div class="container" v-dragula="customers" bag="first-bag">
          <div v-for="customer in customers" :key="customer.id">Customer {{ customer.number }}</div>
        </div>
      </div>
      <div id="target">
        <div v-for="bill in bills">
          <div class="split-header">
            <h3>Bill {{ bill.number }}</h3>
            <div>
              <button v-on:click="removeBill(bill.number)" class="c-btn c-btn--secondary">Remove</button>
            </div>
          </div>
          <div class="container" v-dragula="bill.customers" bag="first-bag">
            <div v-for="customer in bill.customers" :key="customer.id">Customer {{ customer.number }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="sticky-footer">
      <button v-on:click="addBill" class="c-btn c-btn--secondary">Add Bill</button>
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
import Vue from 'vue'
import VueDragula from 'vue-dragula'
import axios from 'axios'

Vue.use(VueDragula);

export default {
  name: 'split',

  data () {
    return {
      customers: [],
      bills: [
        { 'number': 1, 'customers': [] },
        { 'number': 2, 'customers': [] },
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
        'customers': []
      }
      this.bills.push(bill)
    },

    splitOrders: function () {

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
      });
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
    background: #fff;
    border: 1px solid #D0D4D9;
    border-radius: 4px;
    padding: 1rem;
    cursor: move;
    cursor: grab;
    cursor: -moz-grab;
    cursor: -webkit-grab;
    margin-bottom: 10px;

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
