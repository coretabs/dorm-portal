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
      this.$store.dispatch("login")
    }
  }
};