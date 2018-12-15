export default {
  name: "DormInfo",
  components: {
  },
  props:{
    "dorm" : Object
  },
  data: function () {
    return {
      reviews_average: 4.5
    };
  },
  methods: {
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  }
};