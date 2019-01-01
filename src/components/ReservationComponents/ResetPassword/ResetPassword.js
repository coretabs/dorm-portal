export default {
  name: "ResetPassword",
  data: function() {
    return {
      valid: false,
      show: false,
      isPasswordChanged: false,
      isError: false,
      email: '',
      password: '',
      confirmPassword: '',
      passwordRules:[
        v => !!v || this.lang.rules.passRequired,
        v => v.length >= 6 || this.lang.rules.passLength
      ]
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    comparePasswords(){
      return this.password !== this.confirmPassword ? this.lang.resetPassword.noMatch : ''
    }
  },
  methods: {
    submit(){
        let data = {
          userID: this.$route.params.id,
          key: this.$route.params.key,
          password: this.password
        }
        this.$backend.$resetPasswordConfirm(data)
        .then(() => {
          this.isPasswordChanged = true
        })
        .catch(()=>{
          this.isError = true
        })
    },
    formValidate(){
      let isValid = true
      this.passwordRules.forEach((rules) => { if (rules(this.password) !== true) { isValid = false } })
      if(this.password !== this.confirmPassword){ isValid = false }
      this.valid = isValid
    }
  },
  mounted(){
  },
  updated(){
    this.formValidate();
  }
};