export default {
  name: "SingleRoomCard",
  components: {
  },
  props: {
  },
  data: function () {
    return {
      savedRoom: null,
      showSavedRoomModel: false,
      showSavedRoomNav: true
    };
  },
  methods: {
    savedRoomFetch(){
      if(localStorage.getItem("room") != null){
        this.savedRoom = JSON.parse(localStorage.getItem("room"));
        this.showSavedRoomNav = true;
      }
    },
    deleteSavedRoom(){
      localStorage.removeItem("room");
      this.showSavedRoomNav = false;
    },
    showRoomModel(){
      this.showSavedRoomModel = true;
    },
    closeRoomModel(){
      this.showSavedRoomModel = false;
    },
    reserveRoom(roomID){
      localStorage.setItem("room_id", roomID);
      this.$router.push('/reservation');
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  },
  created(){
    this.savedRoomFetch();
  }
};