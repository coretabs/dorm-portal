export default {
  name: "HeaderComponent",
  data: function() {
    return {
      currencies: [{ symbol: "$", code: "USD" }, { symbol: "₺", code: "TL" }],
      languages: [
        { symbol: "English", code: "en" },
        { symbol: "Turkish", code: "tr" }
      ],
      activeBtn: 1,
      showNav: true
    };
  },
  methods: {
    changeLang(lang) {
      this.$store.state.language = lang;
      localStorage.setItem("lang", lang);
    },
    toggleDrawer(){
      this.$store.state.drawer = !this.$store.state.drawer
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  }
};