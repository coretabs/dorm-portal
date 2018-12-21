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