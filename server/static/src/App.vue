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