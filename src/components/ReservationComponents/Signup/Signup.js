export default {
  name: 'Signup',
  data: function(){
    return{
      showRegisterForm: true,
      show: false,
      firstName:'',
      lastName: '',
      email: '',
      valid: false,
      errors: [],
      password: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => v.length >= 3 && v.length <=20 || 'Name must be less than 10 characters'
      ],
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v.trim()) || 'E-mail must be valid'
      ],
      passwordRules:[
        v => !!v || 'Password is required',
        v => v.length >= 8 || 'Password Must be more that 8'
      ]
    }
  },
  methods:{
    submit(){
      if(this.$refs.form.validate()){
        let user = {
          name: this.firstName + ' ' + this.lastName,
          email: this.email,
          password: this.password
        }
        this.$store.dispatch('register', user)
         .then(() => {
            this.showRegisterForm = false
         })
         .catch(err => this.errors = err.response.data)
      }
    },
    redirectToLogin(){
      this.$router.push('login')
    },
    formValidate(){
      let isValid = true

      this.nameRules.forEach((rules) => { if (rules(this.firstName) !== true) { isValid = false } })
      this.nameRules.forEach((rules) => { if (rules(this.lastName) !== true) { isValid = false } })
      this.emailRules.forEach((rules) => { if (rules(this.email) !== true) { isValid = false } })
      this.passwordRules.forEach((rules) => { if (rules(this.password) !== true) { isValid = false } })
      this.valid = isValid
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  },
  updated(){
    this.formValidate();
  }
};