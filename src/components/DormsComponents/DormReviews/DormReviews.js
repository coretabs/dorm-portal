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
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  }
};