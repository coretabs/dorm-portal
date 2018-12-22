
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
      return (localStorage.getItem('room') != null);
    },
    isRoomReserved(){
      const user = JSON.parse(localStorage.getItem('auth'))
      if(user){
        const isReserved = user.reservarion_id
        return isReserved? true : false
      }
      return false
    }
  },
  methods:{
    loadroom(){
      if(this.$store.getters.isLoggedIn){

        const user = JSON.parse(localStorage.getItem('auth'))
        let isReserved = user.reservarion_id
        let step = user.current_step
        let savedRoom = localStorage.getItem('room')
        if(isReserved != null){
          this.$store.dispatch('fetchReservation', isReserved);
        }
        else if(!!savedRoom && step == 2){
          const savedRoom = JSON.parse(localStorage.getItem('room'))
          this.$store.dispatch('reserveRoom', savedRoom.room.id)
          .then(response => {
            localStorage.setItem('auth', JSON.stringify({
              user_name: response.user.name,
              reservarion_id : response.id,
              current_step: response.user.current_step
            }))
            this.$store.dispatch('fetchReservation', response.id)
          })
        }

      }
    }
  },
  mounted(){
    this.loadroom();
  }
};