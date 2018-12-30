import _ from 'lodash'
export default {
  name: "EditRoom",
  props:{
    'roomData': Object,
    'roomId': Number
  },
  data: function () {
    return {
      selectedFeatures:[],
      files: [],
      uploadFiles: [],
      room_types: 1,
      btnDisabled: false,
      isUpdating: false,
      loadingBtn: false,
      roomFilters:{
        radioChoices: [],
        integralChoices: []
      },
      requiredRules: [
        v => !!v || 'This field is required'
      ]
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  },
  methods: {
    remove (item) {
      const index = this.roomData.chosen_features.indexOf(item.id)
      if (index >= 0) this.roomData.chosen_features.splice(index, 1)
    },
    closeEditDialog(){
      this.$emit('closeEditDialog', false)
      this.resetFiles()
    },
    uploadFile(dormId,roomId,formData){
      return this.$store.dispatch("uploadRoomPhotos", {roomId,dormId,formData});
    },
    async submitPhotos(){
      const dormId = localStorage.getItem('manageDormID')
      const roomId = this.roomId
      let success = true
      for (const file of this.uploadFiles) {
        const formData = new FormData()
        if(this.validate(file) === ''){
          formData.set('uploaded_photo', file)
            await this.uploadFile(dormId, roomId, formData).then(()=>{
            this.files.shift()
          }).catch(()=>{
            success = false
          }).then(()=>{
            this.loadingBtn = false
          })
        }
      }
      if(success){
        this.resetFiles()
        this.$store.dispatch('fetchManagerDormRooms',dormId)
        let snackbar = {
          message: 'Room has been Updated successfully',
          color: 'success'
        }
        this.closeEditDialog()
        setTimeout(()=>{
          this.$store.commit('updateSnackbar', snackbar)
        },700)
      }
    },
    submitChanges(){
      const dormId = localStorage.getItem('manageDormID')
      const roomId = this.roomId
      let getRadioArray =  this.roomFilters.radioChoices.map(radioChoices => radioChoices.selected_number);
      let roomData = {
        totalQuota: this.roomData.total_quota,
        allowedQuota: this.roomData.allowed_quota,
        roomTypeId: this.roomData.room_type_id,
        peopleAllowedNumber: this.roomData.people_allowed_number,
        price: this.roomData.price,
        currencyId: this.roomData.price_currency_id,
        confirmationDays: this.roomData.room_confirmation_days,
        durationId: this.roomData.duration_id,
        roomFeatures: this.roomData.chosen_features,
        radioChoices: getRadioArray,
        integralChoices: this.roomFilters.integralChoices
      }

      if(this.$refs.form.validate()){
        this.loadingBtn = true
        this.$store.dispatch('updateRoomData', {dormId,roomId,roomData}).then(()=>{
          this.submitPhotos()
        }).catch((err)=>{
          let snackbar
          if(err.response.status == 403 || err.response.status == 500){
            snackbar = {
              message: 'error occured, please try again',
              color: 'error'
            }
            this.$store.commit('updateSnackbar', snackbar)
          }else{
            snackbar = {
              message: err,
              color: 'error'
            }
            this.$store.commit('updateSnackbar', snackbar)
          }
        }).then(()=>{
          this.loadingBtn = false
        })
      }
    },
    selectNewFile(){
      const files = this.$refs.files.files
      this.uploadFiles = [...this.uploadFiles, ...files]
      this.files = [
        ...this.files,
        ..._.map(files, file => ({
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
    isValid(){
      for(var file of this.uploadFiles) {
        if(this.validate(file) != ''){
          this.btnDisabled = true
          break;
        }
        this.btnDisabled = false
      }
      if(!this.uploadFiles.length){
        this.btnDisabled = false
      }
    },
    removeFile(index){
      this.files.splice(index, 1)
      this.uploadFiles.splice(index, 1)
      this.isValid()
    },
    resetFiles(){
      this.files = []
      this.uploadFiles = []
    },
    addFilter(filterId, optionId, type){
      let filtersArray
      if(type == 'radio'){
        filtersArray = this.roomFilters.radioChoices
      }else{
        filtersArray = this.roomFilters.integralChoices
      }
      let objectUpdated = 0;
      for(const filter of filtersArray){
        if(filter.id == filterId){
          filter.selected_number = optionId
          objectUpdated = -1;
          continue;
        }
      }
      if(objectUpdated == 0){
        filtersArray.push({
          id: filterId,
          selected_number: optionId
        })
      }
    }
  },
  watch: {
    isUpdating (val) {
      if (val) {
        setTimeout(() => (this.isUpdating = false), 3000)
      }
    }
  }
};