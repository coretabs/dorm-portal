
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
      this.progress = this.$store.state.reservationStep;
      return this.$store.state.reservationStep;
      
    }
  }
};