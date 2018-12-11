import FileUpload from 'vue-upload-component/src'

export default {
  name: "ConfirmPayment",
  data: function() {
    return {
      files: []
    };
  },
  components: {
    'file-upload': FileUpload
  },
  methods:{
    submit(){
      this.$store.state.reservationStep++;
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    reservation(){
      return this.$store.state.reservation;
    }
  }
};