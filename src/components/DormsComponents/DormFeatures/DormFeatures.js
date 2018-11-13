export default {
  name: "DormFeatures",
  props:{
    'features': Object,
    'dormName': String
  },
  data: function () {
    return {

    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  }
};