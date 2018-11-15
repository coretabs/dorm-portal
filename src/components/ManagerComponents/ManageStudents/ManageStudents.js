
export default {
  name: "ManageStudents",
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