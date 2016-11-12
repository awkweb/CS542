<template>
  <div id="home-view">
    <div class="c-btn-group">
      <button v-on:click="orderFilter = 'All'" class="c-btn c-btn--secondary">All</button>
      <button v-on:click="orderFilter = 'Open'" class="c-btn c-btn--secondary">Open</button>
      <button v-on:click="orderFilter = 'Closed'" class="c-btn c-btn--secondary">Closed</button>
    </div>
    <router-link :to="{ name: 'order' }" class="c-btn c-btn--primary">New Order</router-link>
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
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}

$DBbutton-background-primary: linear-gradient(color(blue), color(blue, dark)) !default;
$DBbutton-background-primary-hover: color(blue) !default;
$DBbutton-background-primary-active: color(blue, dark) !default;

$DBbutton-background-secondary: color(white) !default;
$DBbutton-background-secondary-hover: linear-gradient(color(white), color(gray, x-light)) !default;
$DBbutton-background-secondary-active: color(gray, x-light) !default;

$DBbutton-background-tertiary: linear-gradient(color(white), color(blue, x-light)) !default;
$DBbutton-background-tertiary-hover: color(blue, x-light) !default;
$DBbutton-background-tertiary-active: linear-gradient(color(blue, x-light), lighten(blue, 5%)) !default;

$DBbutton-background-fallback-primary: color(blue);
$DBbutton-background-fallback-tertiary: color(white);

$DBbutton-text-primary: color(white) !default;
$DBbutton-text-secondary: color(gray) !default;
$DBbutton-text-tertiary: color(blue) !default;

$DBbutton-border-primary: color(blue, dark) !default;
$DBbutton-border-secondary: color(gray, light) !default;
$DBbutton-border-tertiary: color(blue) !default;

.c-btn {
    display: inline-block;
    padding: 7px 12px;

    font-weight: 600;
    line-height: 1.4;
    text-align: center;
    text-decoration: none;

    border: 1px solid currentColor;
    border-radius: 3px;

    cursor: pointer;

    &[disabled], &#{&}--disabled {
        opacity: 0.5;

        cursor: default;
    }

    &:focus {
        box-shadow: 0 0 0 2px color(blue, 0.3);
        outline: none;
    }

    &:hover {
        text-decoration: none;
    }

    &#{&}--big {
        padding: 10px 26px;
    }

    &#{&}--full {
        display: block;
        width: 100%;
    }

    &#{&}--primary {
        color: $DBbutton-text-primary;
        border-color: $DBbutton-border-primary;
        background-color: $DBbutton-background-fallback-primary;
        background: $DBbutton-background-primary;

        &:hover:not(:disabled) {
            background: $DBbutton-background-primary-hover;
        }

        &:active:not(:disabled) {
            background:$DBbutton-background-primary-active;
        }
    }

    &#{&}--secondary {
        color: $DBbutton-text-secondary;
        border-color: $DBbutton-border-secondary;
        background: $DBbutton-background-secondary;

        &:hover:not(:disabled) {
            background: $DBbutton-background-secondary-hover;
        }

        &:active:not(:disabled) {
            background:$DBbutton-background-secondary-active;
        }
    }

    &#{&}--tertiary {
        color: $DBbutton-text-tertiary;
        border-color: $DBbutton-border-tertiary;
        background-color: $DBbutton-background-fallback-tertiary;
        background: $DBbutton-background-tertiary;

        &:hover:not(:disabled) {
            background: $DBbutton-background-tertiary-hover;
        }

        &:active:not(:disabled) {
            background:$DBbutton-background-tertiary-active;
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
