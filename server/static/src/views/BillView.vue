<template>
  <div id="bill-view">
    <h2>View Bills</h2>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'bill',

  data () {
    return {
      bills: []
    }
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
        for (var i in orders) {
          const order = orders[i]
          const billRequest = getBill(order.bill_id)
          billRequests.push(billRequest)
        }

        axios.all(billRequests)
        .then(axios.spread(function (acct, perms) {
          // Both requests are now complete
        }))
      })
      .catch(function (error) {
        console.log(error);
      })
    },

    getBill: function (billId) {
      return axios.get('/api/masterorder', {
        params: {
          id: billId
        }
      })
    }
  },

  watch: {
    '$route': 'getBill'
  },

  created () {
    if (this.$route.params.id)
      this.getBill()
  }
}
</script>

<style lang="sass">

</style>
