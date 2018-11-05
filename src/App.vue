<template>
  <v-app>
    <app-header></app-header>
    <dorm-filter></dorm-filter>
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

</style>
