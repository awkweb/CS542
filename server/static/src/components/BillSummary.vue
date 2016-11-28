<template>
  <div class="bill-summary">
    <span class="semibold">Master Order # {{ masterOrder.id }}</span>
    <span>{{ masterOrder.date | prettyDate }}</span>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  name: 'billSummary',

  props: ['masterOrder'],

  filters: {
    prettyDate: function (dateString) {
      return moment(dateString).add(5, 'hours').format('ddd, MMM D, h:mm a')
    }
  }
}
</script>

<style lang="sass">
.bill-summary {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
  border: 1px solid rgba(37, 40, 43, 0.1);
  border-radius: 3px;
  padding: 10px 15px;

  span {
    display: block;
  font-weight: 500;
  }
}

.semibold {
  color: #007ee5;
}
</style>