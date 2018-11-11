export default {
  name: "DormProfile",
  data: function () {
    return {
      
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  }
};