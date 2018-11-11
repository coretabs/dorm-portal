
import Signup from '../signup/Signup.vue'
import ConfirmPayment from '../confirmPayment/ConfirmPayment.vue'
import Status from '../status/Status.vue'
export default {
  name: "ReservationProcess",
  data: function () {
    return {
      e1: 1
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
    }
  }
};