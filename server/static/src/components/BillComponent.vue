<template>
  <div class="bill-component">
    <div class="bill-header">
      <h3>Bill {{ bill.id }}</h3>
      <span class="bill-total" v-if="bill.orders.length > 1">{{ bill.orders.length }} customers</span>
      <span class="bill-total" v-else>{{ bill.orders.length }} customer</span>
    </div>
    <bill-table v-bind:orders="bill.orders"></bill-table>
  </div>
</template>

<script>
import BillTable from '../components/BillTable.vue'

export default {
  name: 'billComponent',

  props: ['bill'],

  components: {
    'bill-table': BillTable
  }
}
</script>

<style lang="sass">
.bill-header {
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

.bill-component {
  margin-bottom: 60px;

  tr:hover {
    cursor: default;
  }
}
</style>