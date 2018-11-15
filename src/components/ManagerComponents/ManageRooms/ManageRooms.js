
export default {
  name: "ManageRooms",
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