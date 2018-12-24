
export default {
  name: "SelectDorm",
  data: function () {
    return {
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang
    },
    dorms(){
      return this.$store.getters.managerDorms
    }
  },
  methods:{
    chosenDorm(id){
      localStorage.setItem("manageDormID", id);
      this.$store.state.managerDrawerControl = true
      this.$store.state.adminActiveComponent = 'ManageReservations'
    }
  },
  mounted(){
  }
};