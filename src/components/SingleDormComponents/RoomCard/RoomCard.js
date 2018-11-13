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
        grabCursor: true,
        slidesPerView: 'auto',
        centeredSlides: true,
        spaceBetween: 10,
        pagination: {
          el: '.swiper-pagination',
          clickable: true
        },
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev'
        }
      },
      features:  [
        {
          name: "free Wifi",
          icon: "fa-wifi"
      },
      {
          name: "Restaurant",
          icon: "fa-utensils"
      },
      {
          name: "Laundry",
          icon: "local_laundry_service"
      },
      {
        name: "Market",
        icon: "fa-shopping-cart"
      },
      {
        name: "Elevator",
        icon: "fa-check"
      },
      {
        name: "Air condition",
        icon: "fa-wind"
      },
      {
        name: "Fire alarm",
        icon: "fa-fire"
      },
      {
        name: "Barber",
        icon: "fa-cut"
      }       
    ]
    };
  },
  methods: {
    
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  },
  created(){
  }
};