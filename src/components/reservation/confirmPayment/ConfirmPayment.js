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
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  }
};