<template>
  <v-app>
    <app-header></app-header>
  </v-app>
</template>

<script>
  import HeaderComponent from './components/shared/Header'
  export default {
    data: function (){
      return{}
    },
    components: {
      'app-header': HeaderComponent
    }
  }
</script>

<style lang="scss">

</style>
