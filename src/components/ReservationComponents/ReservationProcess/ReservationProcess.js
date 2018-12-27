
import Signup from '../Signup/Signup.vue'
import ConfirmPayment from '../ConfirmPayment/ConfirmPayment.vue'
import Status from '../Status/Status.vue'
export default {
  name: "ReservationProcess",
  data: function () {
    return {
      progress: 0,
      contactDialog: false,
      contact: {}
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
      if(this.$store.getters.reservationStepperState.receiptUploaded){
        this.progress = 3;
      }
      else if(this.$store.getters.reservationStepperState.uploadNewReceipt){
        this.progress = 2;
      }
      else if(this.$store.getters.isLoggedIn){
        const step = JSON.parse(localStorage.getItem('auth'));
        this.progress = step.current_step;
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
    },
    reservationComplated(){
      let reservation = this.$store.getters.reservationData
      return reservation.status == 2 ? true : false
    }
  },
  methods:{
    checkAuth(){
      if(this.$store.getters.isLoggedIn){
        this.$store.dispatch('auth')
        .catch(() => {
          this.$store.dispatch('logout')
          .then(() => {
            this.$router.push('/login')
          })
        })
     }
    },
    loadroom(){
      if(this.$store.getters.isLoggedIn){
        const user = JSON.parse(localStorage.getItem('auth'))
        let isReserved = user.reservarion_id
        let step = user.current_step
        let savedRoom = localStorage.getItem('room')
        if(isReserved != null){
          this.$store.dispatch('fetchReservation', isReserved);
        }
        else if(isReserved == null && !!savedRoom && step == 2){
          const savedRoomData = JSON.parse(localStorage.getItem('room'))
          this.$store.dispatch('reserveRoom', savedRoomData.room)
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
    },
    contactDate(){
      this.contact = this.$store.state.reservation.room_characteristics.dormitory
      this.contactDialog = !this.contactDialog
    }
  },
  mounted(){
    this.checkAuth()
    this.loadroom()
  }
};