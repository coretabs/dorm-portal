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
    },  
    methods: {
    fetchLocale() {
      this.$backend.$fetchLocale().then(responseDate => {
        this.$store.state.currencies = responseDate[0].currencies;
        this.$store.state.languages = responseDate[1].languages;
        console.log(this.$store.state.currencies);
      });
    }
  },
  mounted() {
    this.fetchLocale();
  }
  }
</script>

<style lang="scss">
  .container {
    background: #fff;
  }
</style>
