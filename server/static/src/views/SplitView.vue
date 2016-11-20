<template>
  <div id="split-view">
    <h2 v-if="customers.length > 1">Split {{ customers.length }} Orders</h2>
    <h2 v-else>Split {{ customers.length }} Order</h2>

    <div class="wrapper">
      <div id="source">
        <h3>Customers</h3>
        <div class="container" v-dragula="col1" bag="first-bag">
          <div v-for="text in col1">{{text}}</div>
        </div>
      </div>
      <div id="target">
        <h3>Bill 1</h3>
        <div class="container" v-dragula="col2" bag="first-bag">
          <div v-for="text in col2">{{text}}</div>
        </div>
        <h3>Bill 2</h3>
        <div class="container" v-dragula="col3" bag="first-bag">
          <div v-for="text in col3">{{text}}</div>
        </div>
      </div>
    </div>

    <div class="sticky-footer">
      <button v-on:click="addBill" class="c-btn c-btn--secondary">Add Bill</button>
      <div>
        <button v-on:click="back" class="c-btn c-btn--secondary">Back</button>
        <button v-on:click="splitOrders" class="c-btn c-btn--primary">Finish</button>
      </div>
    </div>
  </div>
</template>

<script>
import router from '../router'
import Vue from 'vue'
import VueDragula from 'vue-dragula'
import axios from 'axios'

Vue.use(VueDragula);

export default {
  name: 'split',

  data () {
    return {
      customers: [],
      col1: [
        'The quick brown fox.',
        'The sly snake.',
        'The hungry hippo.'
      ],
      col2: [
        'The lovely flamingo.',
        'The shrewd llama.',
        'The inquisitive toucan.'
      ],
      col3: [
        'The boisterous lion.',
        'The jaded panda.'
      ],
    }
  },

  methods: {
    back: function () {
      const orderId = this.$route.params.id
      router.push({ name: 'order-update', params: { id: orderId } })
    },

    addBill: function () {
    },

    splitOrders: function () {

    },

    getOrder: function () {
      var vm = this
      const orderId = this.$route.params.id

      axios.get('/api/masterorder', {
        params: {
          id: orderId
        }
      })
      .then(function (response) {
        vm.customers = response.data.orders
      })
      .catch(function (error) {
        console.log(error);
      });
    }
  },

  watch: {
      '$route': 'getOrder'
    },

    created () {
      if (this.$route.params.id)
        this.getOrder()
    }
}
</script>

<style lang="sass">
.wrapper {
  display: flex;
  margin-bottom: 8rem;
}

#source , #target {
  flex: 1;
}

#source {
  padding-right: .5rem;
}

#target {
  padding-left: .5rem;
}

.container {
  margin-bottom: 1rem;
  padding: 1rem;
  background: #F7F9FA;
  border-radius: 4px;

  div {
    background: #fff;
    border: 1px solid #D0D4D9;
    border-radius: 4px;
    padding: 1rem;
    cursor: move;
    cursor: grab;
    cursor: -moz-grab;
    cursor: -webkit-grab;
    margin-bottom: 10px;

    &:hover {
      background: linear-gradient(white, #f7f9fa);
    }

    &:last-child {
      margin-bottom: 0;
    }
  }
}

.container .scale-transition {
  overflow: hidden;
  transition: height .2s;
}

.container .scale-enter {
  height: 0px;
}

.container .scale-leave {
  height: 0px;
}

.gu-mirror {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
  background: #fff;
  transition: opacity 0.4s ease-in-out;
  border: 1px solid #D0D4D9;
  border-radius: 4px;
  cursor: move;
  cursor: grab;
  cursor: -moz-grab;
  cursor: -webkit-grab;
}

.gu-mirror {
  position: fixed !important;
  margin: 0 !important;
  z-index: 9999 !important;
  opacity: 0.8;
  -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=80)";
  filter: alpha(opacity=80);
}

.gu-hide {
  display: none !important;
}

.gu-unselectable {
  -webkit-user-select: none !important;
  -moz-user-select: none !important;
  -ms-user-select: none !important;
  user-select: none !important;
}

.gu-transit {
  opacity: 0.2;
  -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=20)";
  filter: alpha(opacity=20);
}

</style>
