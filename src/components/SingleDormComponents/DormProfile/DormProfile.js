import { swiper, swiperSlide } from 'vue-awesome-swiper'

export default {
  name: "DormProfile",
  components: {
    swiper,
    swiperSlide
  },
  data: function () {
    return {
      lightboxPhotoUrl: '',
      iframe: false,
      lightbox: false,
      model: true,
      swiperOption: {
        slidesPerView: 12,
        centeredSlides: false,
        spaceBetween: 8,
        grabCursor: true,
        preventClicks: false,
        clickable: true,
        pagination: {
          el: '.swiper-pagination',
          clickable: true
        }},
      "name": "Alfam dorm",
      "cover": "https://images.pexels.com/photos/1438072/pexels-photo-1438072.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
      "photos": [
        {
          "is_3d": false,
          "src": "https://images.pexels.com/photos/1438081/pexels-photo-1438081.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
        },
        {
          "is_3d": false,
          "src": "https://images.pexels.com/photos/1326946/pexels-photo-1326946.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
        },
        {
          "is_3d": true,
          "src": "https://momento360.com/e/u/a9b53aa8f8b0403ba7a4e18243aabc66"
        }
      ],
      "geo_longitude": 35.1501,
      "geo_latitude": 33.90111,
      "address": "Kaleland street bla bla",
      "history": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries",
      "contact_email": "alhakeem.prof@gmail.com",
      "contact_number": "00905338524788",
      "facilities": [
        {
          "name": "free Wifi",
          "icon": "fa-wifi"
        },
        {
          "name": "free Wifi",
          "icon": "fa-wifi"
        }
      ],
      "activities": [
        {
          "name": "free Wifi",
          "icon": "fa-wifi"
        },
        {
          "name": "free Wifi",
          "icon": "fa-wifi"
        }
      ],
      "number_of_reviews": 26,
      "reviews_average": 4.5,
      "review": [
        {
          "student_name": "Mohammed Alhakem",
          "stars": 5,
          "description": "I liked the dorm, it is very nice"
        },
        {
          "student_name": "yaser alnajjar",
          "stars": 2,
          "description": "very bad dorm"
        }
      ],
      "rooms": [
        {
          "id": 15225,
          "room_type": "single room",
          "photos": [
            "https://images.pexels.com/photos/279719/pexels-photo-279719.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
            "https://images.pexels.com/photos/1326946/pexels-photo-1326946.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
          ],
          "rooms_left": 5,
          "price": 1500,
          "people_number": 2,
          "facilities": [
            {
              "name": "free Wifi",
              "icon": "fa-wifi"
            },
            {
              "name": "free Wifi",
              "icon": "fa-wifi"
            }
          ]
        }
      ]
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  },
  methods:{
    sendPhotoUrl(url,is_3d){
      this.lightboxPhotoUrl = url
      this.iframe = is_3d
      this.lightbox = !this.lightbox
    }
  }
};