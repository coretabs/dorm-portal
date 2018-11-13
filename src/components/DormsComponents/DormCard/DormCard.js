
import DormMap from "../../SharedComponents/DormMap/DormMap.vue";
import DormReviews from "../DormReviews/DormReviews.vue";

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
    popularFeatures() {
      return this.dorm.features.slice(0, 10);
    },
    lang() {
      return this.$store.getters.lang;
    }
  }
};