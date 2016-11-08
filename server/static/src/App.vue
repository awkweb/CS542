<template>
  <div id="app">
    <h2>Menu</h2>
    <ul v-for="dish in dishes">
      <li>{{ dish.name }}: {{ dish.description }} (${{ dish.cost }})</li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'app',
  data () {
    return {
      dishes: []
    }
  },
  methods: {
    fetchData: function () {
      var dishes = this.dishes
      axios.get('/api/dishes?category=lunch')
        .then(function (response) {
          for (var i in response.data) {
            const dish = response.data[i]
            dishes.push(dish)            
          }
        })
        .catch(function (error) {
          console.log('Error! Could not reach the API. ' + error)
        })
    }
  },
  created: function () {
    this.fetchData()
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
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

a {
  color: #42b983;
}
</style>
