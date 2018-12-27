export default {
  name: 'Status',
  data: function(){
    return{
      status: "",
      statusIcon: ""
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    reservation(){
      switch(this.$store.getters.reservationData.status){
        case '0':
          this.status = "pending"
          this.statusIcon = "fa-clock"
          break;
        case '1':
          this.status = "rejected"
          this.statusIcon = "fa-times"
          break;
        case '2':
          this.status = "confirmed"
          this.statusIcon = "fa-check"
          break;
          case '3':
          this.status = "Wating"
          break;
        case '4':
          this.status = "Updated"
          this.statusIcon = "fa-bell"
          break;
        case '5':
          this.status = "Expired"
          this.statusIcon = "fa-times"
          break;
        default:
          this.status = "Unknown"
          break;
      }
      return this.$store.getters.reservationData
    }
  },
  methods: {
    previousStep(state){
      this.$store.state.reservationStepperState.receiptUploaded = false
      this.$store.state.reservationStepperState.uploadNewReceipt = true
      if(state == 'required'){
        this.$store.state.reservationStepperState.newAmount = true
        this.$store.state.reservationStepperState.uploadDeadline = true
      }else{
        this.$store.state.reservationStepperState.uploadDeadline = false
      }
    }
  }
};