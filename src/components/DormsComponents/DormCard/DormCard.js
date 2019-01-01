
import DormMap from "../../SharedComponents/DormMap/DormMap.vue";
import DormReviews from "../DormReviews/DormReviews.vue";
import DormFeatures from "../DormFeatures/DormFeatures.vue";
import _ from 'lodash'

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
      roomsLeft: this.dorm.number_of_found_rooms,
      dormReviews: []
    }
  },
  methods: {
    showMap() {
      this.mapModel = !this.mapModel;
    },
    showReviews(dormId) {
      this.$backend.$fetchDormReviews(dormId).then((response)=>{
        this.dormReviews = response
      })
      this.reviewsModel = true;
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
    },
    orderedRooms(){
      return _.orderBy(this.dorm.room_characteristics, 'price')
    }
  }
};