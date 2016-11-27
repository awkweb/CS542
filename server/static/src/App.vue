<template>
  <div id="app">
    <!-- header -->
    <header>
      <router-link :to="{ name: 'home' }">Split Bill</router-link>
    </header>
    <!-- main view -->
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'app',

  created () {
    this.$store.dispatch('FETCH_DISHES')
  }
}
</script>

<style lang="sass">
body {
  font-size: 15px;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  max-width: 45rem;
  margin: auto;
}

header {
  display: flex;
  align-items: center;
  height: 50px;
  margin-bottom: 20px;
  border-bottom: 1px solid #EAEAEA;

  a {
    color: #007ee5;
    font-size: 20px;
    font-weight: 700;
    text-decoration: none;
  }
}
</style>