
export default {
  name: "ManageRooms",
  data: function () {
    return {
      quota: 5,
      disableUpdateBtn: true,
      items: [
        { title: 'Edit' },
        { title: 'Delete' }
      ]
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }    
  }
};