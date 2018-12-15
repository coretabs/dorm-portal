export default {
  name: "RoomCard",
  components: {
  },
  props: {
    'room' : Object
  },
  data: function () {
    return {
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
    reserveRoom(room){
      localStorage.setItem("room", JSON.stringify({room}));
      this.$router.push('/reservation');
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  },
  created(){
  }
};