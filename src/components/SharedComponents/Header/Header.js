export default {
  name: "HeaderComponent",
  data: function() {
    return {
      activeBtn: 1,
      showNav: true,
      userName: ''
    };
  },
  methods: {
    changeLang(lang) {
      localStorage.setItem("lang", lang)
      this.$store.state.language = lang
      var date = new Date;
      date.setDate(date.getDate() + 21);
      this.$cookie.set('django_language', lang, { expires: '1Y' });
    },
    changeCurrency(code,symbol){
      this.$store.state.currencyCode = code
      this.$store.state.currencySymbol = symbol
      localStorage.setItem("currency-code", code)
      localStorage.setItem("currency-symbol", symbol)
      this.$store.dispatch('fetchFilters')
    },
    toggleDrawer(){
      this.$store.state.drawer = !this.$store.state.drawer
    },
    logout(){
      this.$store.dispatch('logout')
      .then(() => {
        this.$router.push('/login')
      })
    },
    userRedirect(){
      if(localStorage.getItem('admin')){
        this.$router.push('/manage')
      }
      else{
        this.$router.push('/reservation')
      }
    },
    getUserName(){
      const user = JSON.parse(localStorage.getItem('auth'))
      if(user){
        const fullName = user.user_name.split(' ')
        this.userName = fullName[fullName.length - 1]
      }
    },
    switchDorms(id){
      localStorage.setItem('manageDormID', id)
        this.$store.dispatch('fetchManagerReservation', id)
        this.$store.dispatch('fetchManagerDorm', id)
        this.$store.dispatch('fetchManagerDormRooms', id)
    },
    closeSnackbar(){
      this.$store.state.snackbar.trigger = false
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang
    },
    languages(){
      return this.$store.state.languages
    },
    currencies(){
      return this.$store.state.currencies
    },
    isLogin(){
      return this.$store.getters.isLoggedIn
    },
    isAdmin(){
      return this.$store.getters.isAdmin
    },
    managerDorms(){
      return this.$store.getters.managerDorms
    },
    snackbar(){
      return this.$store.getters.snackbar
    },
    isSelectDormComponent(){
      return this.$store.getters.adminActiveComponent == 'SelectDorm'
    }
  },
  updated(){
    this.getUserName()
  }
};