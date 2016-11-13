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

<style lang="sass">
body {
  font-size: 15px;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  max-width: 47rem;
  margin: auto;
}

header {
  display: flex;
  align-items: center;
  height: 50px;
  margin-bottom: 20px;
  border-bottom: 1px solid #EAEAEA;

  a {
    color: #0073C7;
    font-size: 20px;
    font-weight: 700;
    text-decoration: none;
  }
}
</style>