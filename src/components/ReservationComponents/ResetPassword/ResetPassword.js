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
        v => !!v || 'Password is required',
        v => v.length >= 6 || 'Password Must be more that 6'
      ]
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    comparePasswords(){
      return this.password !== this.confirmPassword ? 'Passwords do not match': ''
    }
  },
  methods: {
    submit(){
        let data = {
          userID: this.$route.params.id,
          key: this.$route.params.key,
          password: this.password
        }
        this.$store.dispatch('resetPasswordConfirm', data)
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