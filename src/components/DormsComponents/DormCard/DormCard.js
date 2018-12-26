
import DormMap from "../../SharedComponents/DormMap/DormMap.vue";
import DormReviews from "../DormReviews/DormReviews.vue";
import DormFeatures from "../DormFeatures/DormFeatures.vue";

export default {
  name: "DormCard",
  components: {
    'dorm-map': DormMap,
    'dorm-reviews': DormReviews,
    'dorm-features': DormFeatures
  },
  props: {
    dorm: {}
  },
  data: function () {
    return {
      roomMode: false,
      room: {},
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
    },
    showRooms(room){
      this.room = room;
      this.roomMode = !this.roomMode;
    },
    closeRoomModel(){
      this.roomMode = !this.roomMode;
    },
    saveRoom(room,id){
      localStorage.setItem("room", JSON.stringify({room}));
      this.$router.push('/dorms/'+id);
    },
    reserveRoom(room){
      if(this.$store.getters.isLoggedIn){
        this.$store.dispatch('reserveRoom', room).then(() => {
          this.$router.push('/reservation')
        })
      }else{
        localStorage.setItem("room", JSON.stringify({room}))
        this.$router.push('/reservation')
      }
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