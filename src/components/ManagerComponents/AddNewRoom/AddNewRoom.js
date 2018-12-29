import FileUpload from 'vue-upload-component/src'
import _ from 'lodash'

export default {
  name: "ManageDorm",
  components: {
    'file-upload': FileUpload
  },
  data: function () {
    return {
      selectedFeatures:[],
      files: [],
      uploadFiles: [],
      isUpdating: false,
      loadingBtn: false,
      roomFilters:{},
      room:{
        totalQuota: null,
        allowedQuota: null,
        roomTypeId: null,
        peopleAllowedNumber: null,
        price: null,
        currencyId: null,
        confirmationDays: null,
        durationId: null,
        integralChoicesHolder: [],
        roomFeatures: [],
        radioChoices:[],
        integralChoices: []
      },
      requiredRules: [
        v => !!v || 'This field is required'
      ]
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  },
  methods: {
    remove (item) {
      const index = this.room.roomFeatures.indexOf(item.id)
      if (index >= 0) this.room.roomFeatures.splice(index, 1)
    },
    fetchRoomFilters(){
      this.$store.dispatch('fetchRoomFilters').then((response)=>{
        this.roomFilters = response
      })
    },
    integralFilter(id,index){
      let value = this.room.integralChoicesHolder[index]
      let objectUpdated = 0;
      for(const filter of this.room.integralChoices){
        if (filter.id === id) {
          filter.selected_number = value;
          objectUpdated = -1;
          continue;
        }
      }
      if(objectUpdated != -1 && value){
        this.room.integralChoices.push({
          id: id,
          selected_number: value
        })
       }
    },
    submitNewRoom(){
      const dormID = localStorage.getItem('manageDormID')
      let roomData = this.room
      if(this.$refs.form.validate()){
        this.loadingBtn = true
        let snackbar
        this.$store.dispatch('addNewRoom', {dormID,roomData}).then(()=>{
          snackbar = {
            message: 'Room has been Add successfully',
            color: 'success'
          }
          this.$refs.form.reset()
        }).catch((err)=>{
          if(err.response.status == 403 || err.response.status == 500){
            snackbar = {
              message: 'error occured, please try again',
              color: 'error'
            }
          }else{
            snackbar = {
              message: err,
              color: 'error'
            }
          }
        }).then(()=>{
          this.$store.commit('updateSnackbar', snackbar)
        })
      }
    },
    selectFile(){
      const files = this.$refs.files.files
      this.uploadFiles = [...this.uploadFiles, ...files]
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
      const MAX_SIZE = 8000000
      const allowedType = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
      if(file.size > MAX_SIZE){
        return `Max size: ${MAX_SIZE/1000}KB`
      }
      if(!allowedType.includes(file.type)){
        return 'File type is not allowed'
      }
      return ''
    },
    removeFile(index){
      this.files.splice(index, 1)
      this.uploadFiles.splice(index, 1)
      this.isValid()
    },
    isValid(){
      for(var file of this.uploadFiles) {
        if(this.validate(file) != ''){
          this.uploaderDisabled = true
          break;
        }
        this.uploaderDisabled = false
      }
    },
    resetFiles(){
      this.files = []
      this.uploadFiles = []
    }
  },
  watch: {
    isUpdating (val) {
      if (val) {
        setTimeout(() => (this.isUpdating = false), 3000)
      }
    }
  },
  mounted(){
    this.fetchRoomFilters()
  }
};