export default {
  name: 'Signup',
  data: function(){
    return{
      showRegisterForm: true,
      show: false,
      firstName:'',
      lastName: '',
      studentId: '',
      email: '',
      valid: false,
      errors: [],
      password: '',
      nameRules: [
        v => !!v || this.lang.rules.nameRequired,
        v => v.length >= 3 && v.length <=20 || this.lang.rules.nameLength
      ],
      emailRules: [
        v => !!v || this.lang.rules.emailRequired,
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v.trim()) || this.lang.rules.emailValid
      ],
      passwordRules:[
        v => !!v || this.lang.rules.passRequired,
        v => v.length >= 6 || this.lang.rules.passLength
      ],
      studentIdRules:[
        v => !!v || this.lang.rules.fieldRequired
      ]
    }
  },
  methods:{
    submit(){
      if(this.studentId != "15700155"){
        this.errors.push([this.lang.signup.wrongIdMsg])
      }
      else{
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