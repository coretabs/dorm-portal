export default {
  name: "HeaderComponent",
  data: function() {
    return {
      activeBtn: 1,
      showNav: true
    };
  },
  methods: {
    fetchFiltersData(){
      this.$backend.$fetchFilters().then(responseDate => {
        this.$store.state.filters = responseDate;
      });
    },
    changeLang(lang) {
      this.$store.state.language = lang;
      localStorage.setItem("lang", lang);
      this.fetchFiltersData();
    },
    changeCurrency(currency){
      this.$store.state.currency = currency;
      localStorage.setItem("currency", currency);
      this.fetchFiltersData();
    },
    toggleDrawer(){
      this.$store.state.drawer = !this.$store.state.drawer
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    languages(){
      return this.$store.state.languages;
    },
    currencies(){
      return this.$store.state.currencies;
    }
  }
};