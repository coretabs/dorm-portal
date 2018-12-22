export default {
  name: "RoomCard",
  components: {
  },
  props: {
    'room' : Object
  },
  data: function () {
    return {};
  },
  methods: {
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
    lang() {
      return this.$store.getters.lang;
    }
  },
  created(){
  }
};