<template>
  <div id="split-view">
    <h2>Split 3 Orders</h2>

    <div class="sticky-footer">
      <button v-on:click="back" class="c-btn c-btn--secondary">Back</button>
      <div>
        <button v-on:click="cancel" class="c-btn c-btn--secondary">Cancel</button>
        <button v-on:click="splitOrders" class="c-btn c-btn--primary">Finish</button>
      </div>
    </div>
  </div>
</template>

<script>
import router from '../router'

export default {
  name: 'split',

  methods: {
    cancel: function () {
      router.push({ name: 'home' })
    },

    back: function () {
      const orderId = this.$route.params.id
      router.push({ name: 'order-update', params: { id: orderId } })
    },

    splitOrders: function () {

    }
  }
}
</script>

<style lang="sass">

</style>
