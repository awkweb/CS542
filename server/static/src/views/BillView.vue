<template>
  <div id="bill-view">
    <h2>View Bills</h2>
    <bill-summary v-bind:masterOrder="masterOrder"></bill-summary>
    <div v-for="bill in bills">
      <bill-component v-bind:bill="bill"></bill-component>
    </div>
  </div>
</template>

<script>
import router from '../router'
import axios from 'axios'

import BillSummary from '../components/BillSummary.vue'
import BillComponent from '../components/BillComponent.vue'

export default {
  name: 'bill',

  data () {
    return {
      bills: [],
      masterOrder: {}
    }
  },

  components: {
    'bill-summary': BillSummary,
    'bill-component': BillComponent
  },

  methods: {
    getBills: function () {
      var vm = this
      const masterOrderId = this.$route.params.id

      axios.get('/api/masterorder', {
        params: {
          id: masterOrderId
        }
      })
      .then(function (response) {
        const orders = response.data.orders
        var billRequests = []
        var orderIds = []
        for (var i in orders) {
          const order = orders[i]
          if (!orderIds.includes(order.bill_id)) {
            const billRequest = vm.getBill(order.bill_id)
            billRequests.push(billRequest)
            orderIds.push(order.bill_id)
          }
        }

        axios.all(billRequests)
        .then(function (responses) {
          for (var i in responses) {
            const bill = responses[i].data
            vm.bills.push(bill)
          }
        })
      })
      .catch(function (error) {
        console.log(error);
      })
    },

    getBill: function (billId) {
      return axios.get('/api/bill', {
        params: {
          id: billId
        }
      })
    },

    getMasterOrder: function () {
      var vm = this
      const orderId = this.$route.params.id

      axios.get('/api/masterorder', {
        params: {
          id: orderId
        }
      })
      .then(function (response) {
        vm.masterOrder = response.data
      })
      .catch(function (error) {
        console.log(error);
      })
    }
  },

  watch: {
    '$route': 'getBill'
  },

  created () {
    if (this.$route.params.id)
      this.getMasterOrder()
      this.getBills()
  }
}
</script>

<style lang="sass">
#bill-view {
  margin-bottom: 8rem;
}
</style>
