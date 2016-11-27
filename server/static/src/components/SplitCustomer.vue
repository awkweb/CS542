<template>
<div>
  <div class="split-header">
    <h3>Bill {{ bill.number }}</h3>
    <div>
      <span class="bill-total">${{ bill.total.toFixed(2) }}</span>
      <button v-on:click="removeBill(bill.number)" class="c-btn c-btn--secondary">Remove</button>
    </div>
  </div>
  <div class="container" v-dragula="bill.customers" bag="bill-bag">
    <div v-for="customer in bill.customers" :key="customer.id">
      <span class="customer-number">Customer {{ customer.number }}</span>
      <span>${{ customer.dishes | total }}</span>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'splitCustomer',

  props: ['bill']
}
</script>

<style lang="sass">

</style>