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
    ],
    photos: [
      "https://images.pexels.com/photos/279719/pexels-photo-279719.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
      "https://images.pexels.com/photos/439227/pexels-photo-439227.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
      "https://images.pexels.com/photos/271734/pexels-photo-271734.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
      "https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
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