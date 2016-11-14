<template>
  <div class="customer-dish">
    <div class="input-wrapper">
        <label class="c-label">Dish</label>
        <select v-model="dish.id" class="c-input">
          <option v-for="item in this.$store.state.dishes" v-bind:value="item.id">{{ item.name }} (${{ item.price }})</option>
        </select>
    </div>

    <div class="input-wrapper">
        <label class="c-label">Quantity</label>
        <input v-model.number="dish.quantity" type="number"  class="c-input">
    </div>

    <div class="button-wrapper">
        <button v-on:click="removeDish" class="c-btn c-btn--secondary">Remove</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'customerDish',
  props: ['dish'],
  methods: {
    removeDish: function () {
      this.$emit('removeDish', this.dish.number)
    },
  }
}
</script>

<style lang="sass">
.customer-dish {
    display: flex;
    align-items: flex-end;
    margin-bottom: 10px;
}

.button-wrapper {
    .c-btn {
        padding: 5px 10px;
        font-size: 12px;
    }
}

.input-wrapper {
    flex: 1;
    padding-right: 10px;
}

.c-label {
    display: block;

    font-size: 12px;

    color: #7b8994;
}

.c-input {
    width: 100%;

    display: block;
    padding: 5px 7px;
    box-sizing: border-box;

    font-size: 13px;
    text-align: left;

    color: #47525d;
    border: 1px solid rgba(37, 40, 43, 0.1);
    border-radius: 3px;
    background-color: white;
    background-clip: padding-box;

    &:focus {
        border-color: #72b6ec;
        outline: 0;
    }

    &:disabled, &.is-disabled {
        background-color: #f7f9fa;
    }

    &.is-invalid,
    .c-form--validated &:invalid {
        background-image: url("../assets/icon-form-invalid.svg");
        background-size: 14px;
        background-position: right 10px center;
        background-repeat: no-repeat;

        padding-right: 34px;

        border-color: #ED1A1E;
        // Override default invalidation styles
        box-shadow: none;
        outline: 0;
    }
    &.is-valid,
    .c-form--validated &:valid {
        background-image: url("../assets/icon-form-valid.svg");
        background-size: 14px;
        background-position: right 10px center;
        background-repeat: no-repeat;

        padding-right: 34px;
    }
}

textarea.c-input {
    resize: vertical;
}

select.c-input {
    background-image: url("../assets/icon-form-dropdown.svg");
    background-size: 7px 14px;
    background-position: right 10px center;
    background-repeat: no-repeat;
    
    -webkit-appearance: none;
    
    padding-right: 27px;
}
</style>