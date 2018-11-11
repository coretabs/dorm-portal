export default {
  name: 'Signup',
  data: function(){
    return{
      show: false
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  }
};