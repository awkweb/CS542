<template>
  <div class="customer-dish">
    <div class="input-wrapper">
        <label class="c-label">Dish</label>
        <select v-bind:id="'select-dish-' + customer.number + '-' + dish.number" v-model="dish.dish_id" placeholder="Select a dish..."></select>
    </div>

    <div class="input-wrapper">
        <label class="c-label">Quantity</label>
        <input v-on:change="changeDish" v-model.number="dish.quantity" type="number" class="c-input">
    </div>

    <div class="button-wrapper">
        <button v-on:click="removeDish" class="c-btn c-btn--secondary">Remove</button>
    </div>
  </div>
</template>

<script>
import selectize from 'selectize/dist/js/selectize'
import $ from 'jquery'

export default {
  name: 'customerDish',

  props: ['dish', 'customer'],

  methods: {
    removeDish: function () {
      this.$emit('removeDish', this.dish)
    },

    changeDish: function () {
      this.$emit('changeDish', this.dish)
    }
  },

  created () {
    var vm = this
    this.$nextTick(function () {
        var groups = []
        var categories = []
        for (var i in this.$store.state.dishes) {
            const dish = this.$store.state.dishes[i]
            if (!categories.includes(dish.category)) {
                const category = dish.category
                groups.push({ 'value': category, 'label': category })
                categories.push(category)
            }
        }

        const id = '#select-dish-' + this.customer.number + '-' + this.dish.number
        $(id).selectize({
            options: this.$store.state.dishes,
            optgroups: groups,
            optgroupField: 'category',
            valueField: 'id',
            labelField: 'name',
            searchField: ['name', 'description'],
            render: {
                option: function(item, escape) {
                    return '<div><div class="item-name"><span>' + escape(item.name) + '</span> <span>$' + escape(item.price.toFixed(2)) + '</span></div> <div class="item-description">' + escape(item.description) + '</div></div>';
                }
            },
            onChange: function(value) {
                vm.dish.dish_id = parseInt(value)
                vm.changeDish()
            },
            onInitialize: function() {
                this.addItem(vm.dish.dish_id)
            }
        })
    })
  }
}
</script>

<style lang="sass">
.optgroup-header {
    padding: 2px 0;
    font-size: 0.85em;
    font-weight: bold;
    text-transform: uppercase;
    border-top: 1px solid #EAEAEA;
    border-bottom: 1px solid #EAEAEA;
}

.item-name {
    display: flex;
    justify-content: space-between;
    color: #000;
}

.customer-dish {
    display: flex;
    align-items: flex-end;
    margin-bottom: 10px;
}

.button-wrapper {
    .c-btn {
        padding: 6px 10px;
        font-size: 12px;
    }
}

.input-wrapper {
    flex: 1;
    padding-right: 6px;
}

.c-label {
    display: block;
    padding-left: 2px;
    font-size: 12px;
    color: #7b8994;
}

.c-input {
    width: 100%;

    display: block;
    padding: 6px 7px;
    box-sizing: border-box;

    font-size: 13px;
    text-align: left;

    color: #47525d;
    border: 1px solid #EAEAEA;
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

input[type=number]::-webkit-inner-spin-button, 
input[type=number]::-webkit-outer-spin-button { 
  -webkit-appearance: none; 
  margin: 0; 
}

// Selectize
.selectize-control {
  position: relative;
  margin-bottom: 2px;
}
.selectize-dropdown,
.selectize-input,
.selectize-input input {
  color: #303030;
  font-family: inherit;
  font-size: 13px;
  line-height: 18px;
  -webkit-font-smoothing: inherit;
}
.selectize-input,
.selectize-control.single .selectize-input.input-active {
  background: #ffffff;
  cursor: text;
  display: inline-block;
}
.selectize-input {
  border: 1px solid #EAEAEA;
  padding: 5px 7px;
  display: inline-block;
  width: 100%;
  position: relative;
  box-shadow: 0;
  box-sizing: border-box;
  border-radius: 3px;
}
.selectize-control.multi .selectize-input.has-items {
  padding: 6px 8px 3px;
}
.selectize-input.full {
  background-color: #ffffff;
}
.selectize-input.disabled,
.selectize-input.disabled * {
  cursor: default !important;
}
.selectize-input.focus {
  border-color: #72b6ec;
}
.selectize-input.dropdown-active {
  border-radius: 3px 3px 0 0;
}
.selectize-input > * {
  vertical-align: baseline;
  display: inline-block;
  zoom: 1;
  *display: inline;
}
.selectize-control.multi .selectize-input > div {
  cursor: pointer;
  margin: 0 3px 3px 0;
  padding: 2px 6px;
  background: #f2f2f2;
  color: #303030;
  border: 0 solid #d0d0d0;
}
.selectize-control.multi .selectize-input > div.active {
  background: #e8e8e8;
  color: #303030;
  border: 0 solid #cacaca;
}
.selectize-control.multi .selectize-input.disabled > div,
.selectize-control.multi .selectize-input.disabled > div.active {
  color: #7d7d7d;
  background: #ffffff;
  border: 0 solid #ffffff;
}
.selectize-input > input {
  display: inline-block !important;
  padding: 0 !important;
  min-height: 0 !important;
  max-height: none !important;
  max-width: 100% !important;
  margin: 0 2px 0 0 !important;
  text-indent: 0 !important;
  border: 0 none !important;
  background: none !important;
  line-height: inherit !important;
  -webkit-user-select: auto !important;
  -webkit-box-shadow: none !important;
  box-shadow: none !important;
}
.selectize-input > input::-ms-clear {
  display: none;
}
.selectize-input > input:focus {
  outline: none !important;
}
.selectize-input::after {
  content: ' ';
  display: block;
  clear: left;
}
.selectize-input.dropdown-active::before {
  content: ' ';
  display: block;
  position: absolute;
  background: #f0f0f0;
  height: 1px;
  bottom: 0;
  left: 0;
  right: 0;
}
.selectize-dropdown {
  position: absolute;
  z-index: 10;
  border: 1px solid #d0d0d0;
  background: #ffffff;
  margin: -1px 0 0 0;
  border-top: 0 none;
  box-sizing: border-box;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border-radius: 0 0 3px 3px;
}
.selectize-dropdown [data-selectable] {
  cursor: pointer;
  overflow: hidden;
}
.selectize-dropdown [data-selectable] .highlight {
  background: rgba(125, 168, 208, 0.2);
  border-radius: 1px;
}
.selectize-dropdown [data-selectable],
.selectize-dropdown .optgroup-header {
  padding: 5px 8px;
}
.selectize-dropdown .optgroup:first-child .optgroup-header {
  border-top: 0 none;
}
.selectize-dropdown .optgroup-header {
  color: #303030;
  background: #ffffff;
  cursor: default;
}
.selectize-dropdown .active {
  background-color: #f5fafd;
  color: #495c68;
}
.selectize-dropdown .active.create {
  color: #495c68;
}
.selectize-dropdown .create {
  color: rgba(48, 48, 48, 0.5);
}
.selectize-dropdown-content {
  overflow-y: auto;
  overflow-x: hidden;
  max-height: 200px;
  -webkit-overflow-scrolling: touch;
}
.selectize-control.single .selectize-input,
.selectize-control.single .selectize-input input {
  cursor: pointer;
}
.selectize-control.single .selectize-input.input-active,
.selectize-control.single .selectize-input.input-active input {
  cursor: text;
}
.selectize-control.single .selectize-input:after {
  content: ' ';
  display: block;
  position: absolute;
  top: 50%;
  right: 10px;
  margin-top: -3px;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 5px 5px 0 5px;
  border-color: #808080 transparent transparent transparent;
}
.selectize-control.single .selectize-input.dropdown-active:after {
  margin-top: -4px;
  border-width: 0 5px 5px 5px;
  border-color: transparent transparent #808080 transparent;
}
.selectize-control .selectize-input.disabled {
  opacity: 0.5;
  background-color: #fafafa;
}
</style>