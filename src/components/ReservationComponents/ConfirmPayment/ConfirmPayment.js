import FlipCountdown from 'vue2-flip-countdown'

export default {
  name: "ConfirmPayment",
  data: function() {
    return {
      file: null
    };
  },
  components: {
    'flip-countdown': FlipCountdown 
  },
  methods:{
    selectFile(){
      this.file = this.$refs.file.files[0]
    },
    submit(id){
      const formData = new FormData()
      formData.append('uploaded_photo', this.file)
      this.$store.dispatch("uploadReceipt", {id,formData})
    },
    removeFile(index){
      this.files.splice(index, 1)
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    reservation(){
      return this.$store.getters.reservationData
    },
    date(){
      return this.$store.state.reservation.confirmation_deadline_date
    }
  },
  updated(){
    
  }
};