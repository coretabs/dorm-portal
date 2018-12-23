import FileUpload from 'vue-upload-component/src'
import FlipCountdown from 'vue2-flip-countdown'

export default {
  name: "ConfirmPayment",
  data: function() {
    return {
      files: []
    };
  },
  components: {
    'file-upload': FileUpload,
    'flip-countdown': FlipCountdown 
  },
  methods:{
    submit(){
      this.$store.state.reservationStep++;
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
    },
    fileSize(){
      let size = file.size | formatSize
    }
  }
};