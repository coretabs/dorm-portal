export default {
  name: "FooterComponent",
  data: function() {
    return {
      
    };
  },
  computed:{
    lang() {
      return this.$store.getters.lang
    }
  }
};