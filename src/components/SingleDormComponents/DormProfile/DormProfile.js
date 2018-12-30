import { swiper, swiperSlide } from 'vue-awesome-swiper'
import DormMap from '../../SharedComponents/DormMap/DormMap.vue';
import RoomCard from '../RoomCard/RoomCard.vue'
import DormInfo from '../DormInfo/DormInfo.vue'
import SingleRoomCard from '../SingleRoomCard/SingleRoomCard.vue'
export default {
  name: "DormProfile",
  components: {
    swiper,
    swiperSlide,
    DormMap,
    RoomCard,
    DormInfo,
    SingleRoomCard
  },
  data: function () {
    return {
      lightboxPhotoUrl: '',
      iframe: false,
      lightbox: false,
      mapModel: false,
      model: true,
      swiperOption: {
        slidesPerView: 10,
        centeredSlides: false,
        spaceBetween: 8,
        grabCursor: true,
        preventClicks: false,
        clickable: true,
        pagination: {
          el: '.swiper-pagination',
          clickable: true
        }},
        dorm:[]
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    checkSavedRoom(){
      return localStorage.getItem("room") != null;
    }
  },
  watch: {
    lang: function () {
      this.fetchDorm()
    }
  },
  methods:{
    sendPhotoUrl(url,is_3d){
      this.lightboxPhotoUrl = url
      this.iframe = is_3d
      this.lightbox = !this.lightbox
    },
    showMap() {
      this.mapModel = !this.mapModel;
    },
    fetchDorm() {
      this.$backend.$fetchDorm(this.$route.params.id, this.$store.state.language, this.$store.state.currencyCode).then(responseDate => {
        this.dorm = responseDate;
      });
    }
  },
  created(){
    this.fetchDorm();
  }
};