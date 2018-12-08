export default {
  name: "HeaderComponent",
  data: function() {
    return {
      activeBtn: 1,
      showNav: true
    };
  },
  methods: {
    changeLang(lang) {
      this.$store.state.language = lang;
      localStorage.setItem("lang", lang);
      this.$store.dispatch('fetchFilters');
    },
    changeCurrency(code,symbol){
      this.$store.state.currency = code;
      localStorage.setItem("currency", code);
      this.$store.dispatch('fetchFilters');
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