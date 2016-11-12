<template>
  <table>
    <thead>
      <th>Order #</th>
      <th>Date</th>
      <th>Status</th>
    </thead>
    <tbody v-for="order in orders">
      <tr v-if="order.status == orderFilter || orderFilter == 'All'">
        <td>{{ order.id }}</td>
        <td>{{ order.date }}</td>
        <td>{{ order.status }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'homeTable',
  props: ['orders', 'orderFilter']
}
</script>
