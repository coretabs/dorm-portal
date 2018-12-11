
import Signup from '../Signup/Signup.vue'
import ConfirmPayment from '../ConfirmPayment/ConfirmPayment.vue'
import Status from '../Status/Status.vue'
export default {
  name: "ReservationProcess",
  data: function () {
    return {
      progress: 0,
      complated: false
    };
  },
  components: {
    'sign-up': Signup,
    'confirm-payment': ConfirmPayment,
    'reservation-status': Status
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    reservationStep(){
      if(this.$store.getters.isLoggedIn){
        const step = JSON.parse(localStorage.getItem('auth'));
        this.progress = step.current_step || 1;
      }else{
        this.progress = 1;
      }
      return this.progress;
    },
    isRoomNotSaved(){
      return (localStorage.getItem('room') == null);
    }
  },
  methods:{
    loadroom(){
      if(this.$store.getters.isLoggedIn){
        const user = JSON.parse(localStorage.getItem('auth'))
        const isReserved = user.reservarion_id
        if(isReserved == null){
          const savedRoom = JSON.parse(localStorage.getItem('room'))
          this.$store.dispatch('reserveRoom', savedRoom.room.id);
          this.$store.dispatch('fetchReservation');
        }
        else{
          this.$store.dispatch('fetchReservation');
        }
      }
    }
  },
  mounted(){
    this.loadroom();
  }
};