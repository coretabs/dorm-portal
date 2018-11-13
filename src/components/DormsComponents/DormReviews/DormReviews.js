export default {
  name: "DormReviews",
  props:{
    'dormName': String
  },
  data: function () {
    return {
      reviews: [
        {
          name: "Mohammed Alhakem",
          stars: 5,
          date: "2/2/2018",
          description: "The place is good especially when it comes to its location and cleanliness. Staff are amazing and very friendly. It is very good compared to the price."
        },
        {
          name: "Mohammed Alhakem",
          stars: 3,
          date: "2/2/2018",
          description: "thanks"
        },
        {
          name: "Mohammed Alhakem",
          stars: 2.5,
          date: "2/2/2018",
          description: "thanks"
        },
        {
          name: "Mohammed Alhakem",
          stars: 4,
          date: "2/2/2018",
          description: "thanks"
        }
      ]
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  }
};