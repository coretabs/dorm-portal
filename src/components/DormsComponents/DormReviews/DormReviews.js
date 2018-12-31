export default {
  name: "DormReviews",
  props:{
    'dormName': String,
    'reviews': Array
  },
  data: function () {
    return {
    }
  },
  methods:{
    maskName(name){
      return name.toLowerCase().split(' ')
      .map((s) => s.charAt(0).toUpperCase() + Array(s.length-1).fill("*").join(''))
      .join(' ');
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  }
};