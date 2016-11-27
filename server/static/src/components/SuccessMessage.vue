<template>
  <div class="success-message">
    <span>Success</span>
    <span v-on:click="close" class="close">&#x00D7</span>
  </div>
</template>

<script>
export default {
  name: 'successMessage',

  props: ['message'],

  methods: {
    close: function () {
        this.$emit('closeAlert')
    }
  }
}
</script>

<style lang="sass">
.success-message {
    display: flex;
    justify-content: space-between;
    color: #2c683f;
    background: #edfaf1;
    border: 1px solid rgba(44, 104, 63, 0.44);
    border-radius: 3px;
    padding: 10px 15px;
    font-weight: 500;

    .close {
        cursor: pointer;
    }
}
</style>