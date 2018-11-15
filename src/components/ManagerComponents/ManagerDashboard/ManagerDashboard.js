
export default {
  name: "ManagerDashboard",
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