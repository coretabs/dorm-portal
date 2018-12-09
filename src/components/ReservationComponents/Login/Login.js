export default {
  name: "Login",
  data: function() {
    return {
      show: false,
      password: "Password"
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  },
  methods: {
    submit(){
      this.$store.dispatch("login").then(response => {
        if(response.is_manager == true){
          this.$router.push('/manage')
        }
        else{
          this.$router.push('/reservation')
        }
      })
      .catch(function (error) {
        
      });
    }
  }
};