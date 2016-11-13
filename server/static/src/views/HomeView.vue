<template>
  <div id="home-view">
    <h2>{{ orderFilter }} Orders</h2>
    <div class="toolbar">
        <div class="c-btn-group">
          <button v-on:click="orderFilter = 'All'" class="c-btn c-btn--secondary">All</button>
          <button v-on:click="orderFilter = 'Open'" class="c-btn c-btn--secondary">Open</button>
          <button v-on:click="orderFilter = 'Closed'" class="c-btn c-btn--secondary">Closed</button>
        </div>
        <div class="c-btn-group right">
            <router-link :to="{ name: 'order' }" class="c-btn c-btn--primary">New Order</router-link>
        </div>
    </div>
    <order-table v-bind:orders="orders" v-bind:orderFilter="orderFilter"></order-table>
  </div>
</template>

<script>
import OrderTable from '../components/OrderTable.vue'
import axios from 'axios'

export default {
  name: 'home',
  data () {
    return {
      orders: [],
      orderFilter: 'All'
    }
  },
  components: {
    'order-table': OrderTable
  },
  methods: {
    fetchData: function () {
      var vm = this;
      axios.get('/api/masterorder/all')
        .then(function (response) {
          vm.orders = response.data;
        })
        .catch(function (error) {
          console.log('Error! Could not reach the API. ' + error)
        })
    }
  },
  created: function () {
    this.fetchData();
  }
}
</script>

<style lang="sass">
.toolbar {
    display: flex;
    margin-bottom: 30px;

    .c-btn-group {
        display: inline-flex;
        flex: 1;
    }

    .right {
        display: flex;
        justify-content: flex-end;
    }
}

.c-btn {
    display: inline-block;
    padding: 7px 20px;

    font-size: 13px;
    font-weight: 600;
    line-height: 1.4;
    text-align: center;

    border: 1px solid currentColor;
    border-radius: 3px;
    text-decoration: none;

    cursor: pointer;

    &[disabled], &#{&}--disabled {
        opacity: 0.5;

        cursor: default;
    }

    &:focus {
        box-shadow: 0 0 0 2px color(blue, 0.3);
        outline: none;
    }

    &#{&}--primary {
        color: #fff;
        border-color: #0071ce;
        background: #007ee5;

        &:hover:not(:disabled) {
            background: linear-gradient(#007ee5, #0071ce);
        }

        &:active:not(:disabled) {
            background: #0071ce;
        }
    }

    &#{&}--secondary {
        color: #47525d;
        border-color: #D0D4D9;
        background: #fff;

        &:hover:not(:disabled) {
            background: linear-gradient(white, #f7f9fa);
        }

        &:active:not(:disabled) {
            background: #F7F9FA;
        }
    }
}

.c-btn-group {
    display: flex;

    .c-btn {
        margin: 0;
        border-radius: 0;

        + .c-btn {
            border-left: 0;
        }

        &:first-child {
            border-top-left-radius: 3px;
            border-bottom-left-radius: 3px;
        }

        &:last-child {
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }
    }

    &--justify {
        width: 100%;

        .c-btn {
            flex: 1 0 auto;
        }
    }
}
</style>
