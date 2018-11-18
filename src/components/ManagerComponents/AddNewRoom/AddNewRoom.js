export default {
  name: "ManageDorm",
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