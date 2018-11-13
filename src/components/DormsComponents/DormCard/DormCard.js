
import DormMap from "../../SharedComponents/DormMap/DormMap.vue";
import DormReviews from "../DormReviews/DormReviews.vue";
import DormFeatures from "../DormFeatures/DormFeatures.vue";

export default {
  name: "DormCard",
  components: {
    "dorm-map": DormMap,
    "dorm-reviews": DormReviews,
    'dorm-features': DormFeatures
  },
  props: {
    dorm: {}
  },
  data: function () {
    return {
      mapModel: false,
      reviewsModel: false,
      featuresModel: false,
      roomsLeft: this.dorm.number_of_found_rooms
    };
  },
  methods: {
    showMap() {
      this.mapModel = !this.mapModel;
    },
    showReviews() {
      this.reviewsModel = !this.reviewsModel;
    },
    showFeatures(){
      this.featuresModel = !this.featuresModel;
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