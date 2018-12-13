export default {
  name: "ConfirmAccount",
  data: function() {
    return {
      isConfirmed: null,
      alert: false,
      email: '',
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v.trim()) || 'E-mail must be valid'
      ]
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  },
  methods: {
    verifyEmail(){
      this.$store.dispatch("verifyEmail", this.$route.params.key)
      .then(()=>{
        this.isConfirmed = true
      })
      .catch(() => {
        this.isConfirmed = false
        this.alert = true
      })
    
    }
  },
  mounted(){
    this.verifyEmail();
  }
};