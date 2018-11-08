<template>
  <v-app>
    <router-view></router-view>
    <app-header></app-header>
  </v-app>
</template>

<script>
  import HeaderComponent from './components/shared/Header'
  import DormFilter from './components/dorms/DormFilter'
  export default {
    data: function (){
      return{}
    },
    components: {
      'app-header': HeaderComponent,
      'dorm-filter': DormFilter
    }
  }
</script>

<style lang="scss">
  .container {
    background: #fff;
  }
</style>
