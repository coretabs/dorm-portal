export default {
  name: 'Signup',
  data: function(){
    return{
      show: false,
      showSignup: false
    }
  },
  methods:{
    submit(){
      this.$store.state.reservationStep++;
    },
    login(){
      this.$store.dispatch('login');
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  }
};