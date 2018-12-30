import _ from 'lodash'

export default {
  name: "EditRoom",
  props:{
    'roomData': Object
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
    },
    currencyId(){
      return this.roomData.price_currency * 1
    }
  },
  methods: {
    remove (item) {
      const index = this.room.roomFeatures.indexOf(item.id)
      if (index >= 0) this.room.roomFeatures.splice(index, 1)
    },
    async submitPhotos(roomId){
      const dormId = localStorage.getItem('manageDormID')
      let success = true
      for (const file of this.uploadFiles) {
        this.loadingBtn = true
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
        this.files = []
        this.uploadFiles = []
        this.$store.dispatch('fetchManagerDormRooms',dormId)
        let snackbar = {
          message: 'Room has been Add successfully',
          color: 'success'
        }
        this.$refs.form.reset()
        this.$store.commit('updateSnackbar', snackbar)
        }
      },
      //submit room
      selectFile(){
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
      },
      removeFile(index){
        this.files.splice(index, 1)
        this.uploadFiles.splice(index, 1)
        this.isValid()
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
  }
};