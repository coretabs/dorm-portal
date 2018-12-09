export default {
  name: 'Signup',
  data: function(){
    return{
      show: false
    }
  },
  methods:{
    submit(){
      this.$store.state.reservationStep++;
    },
    redirectToLogin(){
      this.$router.push('login')
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  }
};