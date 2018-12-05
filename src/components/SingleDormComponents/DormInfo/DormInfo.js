import { swiper, swiperSlide } from 'vue-awesome-swiper'
export default {
  name: "DormInfo",
  components: {
    swiper,
    swiperSlide
  },
  data: function () {
    return {
      swiperOption: {
        grabCursor: true,
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        autoplay: {
          delay: 5000,
        },
        pagination: {
          el: '.swiper-pagination',
          clickable: true
        }
      },
      history:'We believe that staying in a dormitory where all types of technological, cultural and sportive facilities are offered under campus safety, will be a best start for your academic life. \n\n  In an ideal world this website wouldn’t exist, a client would acknowledge the importance of having web copy before the design starts. Needless to say it’s very important, content is king and people are beginning to understand that.',
      contact_email: 'alhakeem.prof@gmail.com',
      contact_number: '00905338524788',
      reviews_average: 4.5,
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
        },
        
    ]
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