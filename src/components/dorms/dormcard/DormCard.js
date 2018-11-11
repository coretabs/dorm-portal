
import DormMap from "../dormmap/DormMap.vue";
import DormReviews from "../DormReviews";

export default {
  name: "DormCard",
  components: {
    "dorm-map": DormMap,
    "dorm-reviews": DormReviews
  },
  props: {
    dorm: {}
  },
  data: function () {
    return {
      mapModel: false,
      reviewsModel: false,
      roomsLeft: this.dorm.number_of_found_rooms
    };
  },
  methods: {
    showMap() {
      this.mapModel = !this.mapModel;
    },
    showReviews() {
      this.reviewsModel = !this.reviewsModel;
    }
  },
  computed: {
    popularFacilities() {
      return this.dorm.facilities.slice(0, 4);
    },
    popularActivities() {
      return this.dorm.activities.slice(0, 4);
    },
    lang() {
      return this.$store.getters.lang;
    }
  }
};