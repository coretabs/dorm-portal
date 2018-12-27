import FlipCountdown from 'vue2-flip-countdown'
import _ from 'lodash'
import Axios from 'axios';

export default {
  name: "ConfirmPayment",
  data: function() {
    return {
      loadingBtn: false,
      files: [],
      uploadFiles: [],
      disabled: false
    };
  },
  components: {
    'flip-countdown': FlipCountdown 
  },
  methods:{
    selectFile(){
      const files = this.$refs.files.files
      this.uploadFiles = [...this.files, ...files]
      this.files = [
        ...this.files,
        ..._.map(files, file=>({
          name: file.name,
          size: file.size,
          type: file.type,
          invalidMessage: this.validate(file)
        }))
      ]
      this.isValid()
    },
    validate(file){
      const MAX_SIZE = 200000
      const allowedType = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
      if(file.size > MAX_SIZE){
        return `Max size: ${MAX_SIZE/1000}KB`
      }
      if(!allowedType.includes(file.type)){
        return 'File type is not allowed'
      }
      return ''
    },
    uploadFile(id, formData){
      return this.$store.dispatch("uploadReceipt", {id,formData});
    },
    async submit(id){
      let success = true
      for (const file of this.uploadFiles) {
        this.loadingBtn = true
        const formData = new FormData()
        if(this.validate(file) === ''){
          formData.set('uploaded_photo', file)
          await this.uploadFile(id, formData).then(()=>{
            console.log(formData.get('uploaded_photo'))
            this.files.shift()
          }).catch((err)=>{
            console.log(err)
            success = false
          })
        }
      }
      this.loadingBtn = false
      if(success){
        let snackbar = {
          message: 'Files Uploaded successfully',
          color: 'success'
        }
        this.$store.commit('updateSnackbar', snackbar)
      }else{
        let snackbar = {
          message: 'Something went Wrong!',
          color: 'error'
        }
        this.$store.commit('updateSnackbar', snackbar)
      }

      // this.files = []
      // this.uploadFiles = []
    },
    removeFile(index){
      this.files.splice(index, 1)
      this.uploadFiles.splice(index, 1)
      this.isValid()
    },
    isValid(){
      for(var file of this.uploadFiles) {
        if(this.validate(file) != ''){
          this.disabled = true
          break;
        }
        this.disabled = false
      }
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
  }
};