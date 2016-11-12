<template>
  <div>
    <select v-model="dish.id">
      <option v-for="item in this.$store.state.dishes" v-bind:value="item.id">{{ item.name }} (${{ item.price }})</option>
    </select>
    <input v-model.number="dish.quantity" type="number">
  </div>
</template>

<script>
export default {
  name: 'customerDish',
  props: ['dish']
}
</script>
