import DormMap from "../../SharedComponents/DormMap/DormMap.vue";
import _ from 'lodash'

export default {
  name: "ManageDorm",
  components: {
    'dorm-map': DormMap
  },
  data: function () {
    return {
      active: null,
      items: ['Streaming', 'Eating'],
      selectedFeatures: [],
      files: [],
      uploadFiles: [],
      uploaderDisabled: false,
      isUpdating: false,
      loadingBtn: false,
      file: '',
      search: '',
      headers: [
        { text: 'id', value: 'id' },
        { text: 'Bank Name', value: 'bank_name'  },
        { text: 'Account Name', value: 'account_name' },
        { text: 'Account Number', value: 'account_number' },
        { text: 'Swift', value: 'swift' },
        { text: 'IBAN', value: 'iban' },
        { text: 'Currency', value: 'currency_code' },
        { text: 'Actions', value: 'id' }
      ],
      lightBox:{
        url: '',
        isIframe: false,
        isAdd: false,
        is360: false
      },
      bank:{
        name:'',
        accountName:'',
        accountNumber: '',
        swift:'',
        iban: '',
        currency: ''
      },
      dialog: {
        idHolder: null,
        isEdit: false,
        general: false,
        features: false,
        location: false,
        addBanks: false,
        photos: false
      },
      deleteRecord:{
        confirmDialog: false,
        id: null
      },
      rowsPerPage: [10, 20, 30, 40],
      pagination: {
        rowsPerPage: 10,
        sortBy: 'id',
        descending : true
      },
      dormsAboutDesc:[1,2],
      requiredRules:[
        v => !!v || 'This field is required'
      ],
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid'
      ],
      urlRules:[
        v => !!v || 'URL is required',
        v => /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/.test(v) || 'URL must be valid, Ex: https://emu.edu.tr'
      ]
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang
    },
    languages(){
      return this.$store.state.languages
    },
    currencies(){
      return this.$store.state.currencies
    },
    dorm(){
      return this.$store.getters.manageDorm
    },
    bankAccounts(){
      return this.dorm.bank_accounts
    }
  },
  methods: {
    remove (item) {
      const index = this.selectedFeatures.indexOf(item.id)
      if (index >= 0) this.selectedFeatures.splice(index, 1)
    },
    resetFields(obj) {
      Object.keys(obj).forEach((key)=> {
          obj[key] = null
      })
    },
    fetchManagerDorm(){
      //  
      const dormID = localStorage.getItem('manageDormID')
      this.$store.dispatch("fetchManagerDorm", dormID)
      .catch(()=>{
        this.$store.state.snackbar.trigger = true
        this.$store.state.snackbar.message = 'Can\'t load dorm'
        this.$store.state.snackbar.color = 'error'
      })
    },
    formBind(dialogName,data){
      this.dialog['isEdit'] = true
      if(dialogName == 'addBanks'){
        this.dialog.idHolder = data.id
        this.bank.name = data.bank_name
        this.bank.accountName = data.account_name
        this.bank.accountNumber = data.account_number
        this.bank.swift = data.swift
        this.bank.currency = data.currency_code
        this.bank.iban = data.iban        
      }
    },
    updateDialog(dialogName, editAction, data){
      if(editAction == true){
        this.formBind(dialogName, data)
      }else{
        this.dialog['isEdit'] = false
      }
      if(dialogName == 'features'){
        this.selectedFeatures = this.$store.state.dormFeatures
      }
      this.dialog[dialogName] = true
    },
    closeDialog(dialogName){
      this.dialog[dialogName] = false
      if(dialogName == 'addBanks'){
        this.$refs.form.reset()
      }
    },
    UpdateDormInfo(data,dialog){
      if(this.$refs.form.validate()){
        this.loadingBtn = true
        this.$store.dispatch("updateDormInfo", data).then(()=>{
          let snackbar = {
            message: 'Updeated successfully',
            color: 'success'
          }
          const dormID = localStorage.getItem('manageDormID')
          this.$store.dispatch("fetchManagerDorm", dormID)
          this.closeDialog(dialog)
          this.$store.commit('updateSnackbar', snackbar)
        }).catch(()=>{
          let snackbar = {
            message: 'Something went wrong!, try again',
            color: 'error'
          }
          this.$store.commit('updateSnackbar', snackbar)
        }).then(()=>{
          this.loadingBtn = false
        })
      }
    },
    submitDormInfo(dialog){
      let about = []
      for(const lang in this.dorm.abouts){
        about.push({
          [lang] : this.dorm.abouts[lang]
        })
      }
      let data = {
        dormID: localStorage.getItem('manageDormID'),
        abouts: about,
        contact_name: this.dorm.contact_name,
        contact_number: this.dorm.contact_number,
        contact_fax: this.dorm.contact_fax,
        contact_email: this.dorm.contact_email,
      }
      this.UpdateDormInfo(data, dialog)
    },
    submitDormFeatures(dialog){
      let data = {
        dormID: localStorage.getItem('manageDormID'),
        features: this.selectedFeatures
      }
      this.UpdateDormInfo(data, dialog)
    },
    getGeolocation(){
      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition((position)=>{
          position.enableHighAccuracy = true
          console.log(position)
          const lng = position.coords.longitude
          const lat = position.coords.latitude
          this.dorm.geo_longitude = lng
          this.dorm.geo_latitude = lat
        })
      } else {
        console.log('geolocation IS NOT available on your browser');
      }
    },
    submitDormLocation(dialog){
      let data = {
        dormID: localStorage.getItem('manageDormID'),
        geo_longitude: this.dorm.geo_latitude,
        geo_latitude: this.dorm.geo_longitude,
        address: this.dorm.address
      }
      this.UpdateDormInfo(data, dialog)
    },
    selectCover(){
      const file = this.$refs.coverFile.files[0]
      this.file = file
      
      const MAX_SIZE = 20000000
      const allowedType = ['image/jpeg', 'image/png', 'image/gif']
      const largeFile = file.size > MAX_SIZE
      const isAllowedType = allowedType.includes(file.type)
      const id = localStorage.getItem('manageDormID')
      const formData = new FormData()
      formData.append('cover', this.file)

      if(isAllowedType && !largeFile){
        this.$store.dispatch("uploadDormCover", {id,formData}).then(()=>{
          let snackbar = {
            message: 'Cover Updated Successfully',
            color: 'success'
          }
          const dormID = localStorage.getItem('manageDormID')
          this.$store.commit('updateSnackbar', snackbar)
          this.$store.dispatch("fetchManagerDorm", dormID)
        }).catch(()=>{
          let snackbar = {
            message: 'Some thing went wrong! try again',
            color: 'error'
          }
          this.$store.commit('updateSnackbar', snackbar)
        })
      }else{
        let message = isAllowedType ? `Max size is  ${MAX_SIZE/1000} KB` : 'Only images are allowed'
        let snackbar = {
          message: message,
          color: 'error'
        }
        this.$store.commit('updateSnackbar', snackbar)
      }      
    },
    submitNewBank(){
      const id = localStorage.getItem('manageDormID')
      let data = this.bank
      if(this.$refs.form.validate()){
        this.$store.dispatch("addBankAccount", {id, data}).then(() => {
          let snackbar = {
            message: 'Bank Account Added Successfully',
            color: 'success'
          }
          this.$store.dispatch("fetchManagerDorm", id)
          this.closeDialog('addBanks')
          this.$store.commit('updateSnackbar', snackbar)
        }).catch(() => {
          let snackbar = {
            message: 'Some thing went wrong! try again',
            color: 'error'
          }
          this.$store.commit('updateSnackbar', snackbar)
        })
      }
    },
    deleteBankAccount(){
      const accountId= this.deleteRecord.id
      const dormId = localStorage.getItem('manageDormID')
      this.$store.dispatch('deleteBankAccount', {dormId,accountId}).then(()=>{
        let snackbar = {
          message: 'Bank Account Has been Deleted Successfully',
          color: 'success'
        }
        this.$store.dispatch("fetchManagerDorm", dormId)
        this.deleteRecord.confirmDialog = false
        this.$store.commit('updateSnackbar', snackbar)
      }).catch(()=>{
        let snackbar = {
          message: 'Some thing went wrong! try again',
          color: 'error'
        }
        this.$store.commit('updateSnackbar', snackbar)
      })
    },
    confirmDelete(id){
      this.deleteRecord.confirmDialog = true
      this.deleteRecord.id = id
    },
    updateBankAccount(){
      const dormId = localStorage.getItem('manageDormID')
      const accountId = this.dialog.idHolder
      let data = this.bank
      if(this.$refs.form.validate()){
        this.$store.dispatch("updateBankAccount", {dormId, accountId, data}).then(() => {
          let snackbar = {
            message: 'Bank Account Updated Successfully',
            color: 'success'
          }
          this.$store.dispatch("fetchManagerDorm", dormId)
          this.closeDialog('addBanks')
          this.$store.commit('updateSnackbar', snackbar)
        }).catch(() => {
          let snackbar = {
            message: 'Some thing went wrong! try again',
            color: 'error'
          }
          this.$store.commit('updateSnackbar', snackbar)
        })
      }
    },
    openPhotosDialog(url,is_3d,isAdd = false){
      this.lightBox.url = url
      this.lightBox.isIframe = is_3d
      this.lightBox.isAdd = isAdd
      this.dialog.photos = true
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
      const MAX_SIZE = 200000
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
    },
    uploadFile(id, formData){
      return this.$store.dispatch("uploadPhotos", {id,formData});
    },
    async submitPhotos(){
      const dormId = localStorage.getItem('manageDormID')
      let success = true
      for (const file of this.uploadFiles) {
        this.loadingBtn = true
        const formData = new FormData()
        if(this.validate(file) === ''){
          formData.set('uploaded_photo', file)
          await this.uploadFile(dormId, formData).then(()=>{
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
        let snackbar = {
          message: 'Files Uploaded successfully',
          color: 'success'
        }
        this.$store.commit('updateSnackbar', snackbar)
        this.$store.dispatch('fetchManagerDorm', dormId)
        this.closeDialog('photos')
      }else{
        let snackbar = {
          message: 'Something went Wrong!',
          color: 'error'
        }
        this.$store.commit('updateSnackbar', snackbar)
      }
    },
    submit360Photos(){
      if(this.$refs.form.validate()){
        const dormId = localStorage.getItem('manageDormID')
        let data = {
          is360Photo: true,
          url: this.lightBox.url
        }
        this.$store.dispatch('upload360Photos',{dormId,data}).then(()=>{
          let snackbar = {
            message: 'Files Uploaded successfully',
            color: 'success'
          }
          this.$store.commit('updateSnackbar', snackbar)
          this.$store.dispatch('fetchManagerDorm', dormId)
          this.closeDialog('photos')
        }).catch(()=>{
          let snackbar = {
            message: 'Something went Wrong!',
            color: 'error'
          }
          this.$store.commit('updateSnackbar', snackbar)
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
  },
  mounted(){
    this.fetchManagerDorm()
  }
};