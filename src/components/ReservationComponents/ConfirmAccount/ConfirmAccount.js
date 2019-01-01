export default {
  name: "ConfirmAccount",
  data: function() {
    return {
      isConfirmed: false,
      isNotConfirmed: false,
      isExpiredLink: false,
      isEmailNotExist: false,
      valid: false,
      emailSent: false,
      email: '',
      emailRules: [
        v => !!v || this.lang.resendActivationEmail.emailRule,
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
      this.$backend.$verifyEmail(this.$route.params.key)
      .then(()=>{
        this.isConfirmed = true
      })
      .catch(() => {
        this.isNotConfirmed = true
        this.isExpiredLink = true
      })
    },
    formValidate(){
      let isValid = true
      this.emailRules.forEach((rules) => { if (rules(this.email) !== true) { isValid = false } })
      this.valid = isValid
    },
    submit(){
      if(this.$refs.form.validate()){
        let email= this.email
        this.$backend.$resendVerifyEmail(email)
         .then(() => {
            this.emailSent = true
            this.isExpiredLink = false
            this.isEmailNotExist = false
         })
         .catch(() => {
            this.isEmailNotExist = true
            this.isExpiredLink = false
         })
      }
    }
  },
  mounted(){
    this.verifyEmail();
  },
  updated(){
    this.formValidate();
  }
};