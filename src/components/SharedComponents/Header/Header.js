export default {
  name: "HeaderComponent",
  data: function() {
    return {
      currencies: [{ symbol: "$", code: "USD" }, { symbol: "₺", code: "TL" }],
      languages: [
        { symbol: "English", code: "en" },
        { symbol: "Turkish", code: "tr" }
      ]
    };
  },
  methods: {
    changeLang(lang) {
      this.$store.state.language = lang;
      localStorage.setItem("lang", lang);
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  }
};