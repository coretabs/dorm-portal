<template>
  <v-app>
    <router-view></router-view>
    <app-header></app-header>
    <app-footer></app-footer>
  </v-app>
</template>

<script>
  import HeaderComponent from './components/SharedComponents/Header/Header.vue'
  import DormFilter from './components/DormsComponents/DormFilter/DormFilter.vue'
  import FooterComponent from './components/SharedComponents/Footer/Footer.vue'
  export default {
    data: function (){
      return{}
    },
    components: {
      'app-header': HeaderComponent,
      'dorm-filter': DormFilter,
      'app-footer': FooterComponent
    }
  }
</script>

<style lang="scss">
  .container {
    background: #fff;
  }
</style>
