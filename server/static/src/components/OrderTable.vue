<template>
  <table class="c-table">
    <thead>
      <th>Order #</th>
      <th>Date</th>
      <th>Customers</th>
      <th>Total</th>
      <th>Status</th>
    </thead>
    <tbody v-for="order in orders">
      <tr v-if="order.status == orderFilter || orderFilter == 'All'" v-on:click="handleClick(order.id, order.status)">
        <td>{{ order.id }}</td>
        <td>{{ order.date | prettyDate }}</td>
        <td>3</td>
        <td>$27.50</td>
        <td>{{ order.status }}</td>
      </tr>
    </tbody>  
  </table>
</template>

<script>
import router from '../router'
import moment from 'moment'

export default {
  name: 'homeTable',
  
  props: ['orders', 'orderFilter'],

  methods: {
    handleClick: function (orderId, orderStatus) {
      // if (orderStatus === 'Open')
      //   router.push({ name: 'order-update', params: { id: orderId }})
      router.push({ name: 'order-update', params: { id: orderId }})
    }
  },
  
  filters: {
    prettyDate: function (dateString) {
      return moment(dateString).fromNow();
    }
  }
}
</script>

<style lang="sass">
table {
  margin-bottom: 23px;
}

table {
  border-collapse: collapse;
}

.c-table {
  display: table;
  width: 100%;
  text-align: left;

  tr:hover {
    background: #f7f9fa;
    cursor: pointer;
  }
}

.c-table__th, .c-table th, .c-table__td, .c-table td {
  padding-top: 11.5px;
  padding-bottom: 11.5px;
  padding-left: 5.75px;
  padding-right: 5.75px;
}

.c-table__th, .c-table th {
  font-weight: 600;
  color: #737373;
  border-bottom: 2px solid #d0d4d9;
}

.c-table__row, .c-table tr {
  border-bottom: 1px solid #d0d4d9;
}
</style>
