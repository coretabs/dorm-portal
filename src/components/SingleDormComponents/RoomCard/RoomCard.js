import { swiper, swiperSlide } from 'vue-awesome-swiper'
export default {
  name: "RoomCard",
  components: {
    swiper,
    swiperSlide
  },
  props: {
  },
  data: function () {
    return {
      swiperOption: {
        slidesPerView: 1,
        pagination: {
          el: '.swiper-pagination',
          clickable: true
        },
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev'
        }
      }
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