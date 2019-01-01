import _ from 'lodash'
export default {
  name: "EditRoom",
  props: {
    'roomData': Object,
    'roomId': Number
  },
  data: function () {
    return {
      selectedFeatures: [],
      files: [],
      uploadFiles: [],
      room_types: 1,
      btnDisabled: false,
      isUpdating: false,
      loadingBtn: false,
      roomFilters: {
        radioChoices: [],
        integralChoices: []
      },
      deletePhoto: {
        id: null,
        confirmDialog: false
      },
      requiredRules: [
        v => !!v || this.lang.rules.fieldRequired
      ]
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  },
  methods: {
    remove(item) {
      const index = this.roomData.chosen_features.indexOf(item.id)
      if (index >= 0) this.roomData.chosen_features.splice(index, 1)
    },
    closeEditDialog() {
      this.$emit('closeEditDialog', false)
      this.resetFiles()
    },
    uploadFile(dormId, roomId, formData) {
      return this.$backend.$uploadRoomPhotos(dormId, roomId, formData);
    },
    async submitPhotos() {
      const dormId = localStorage.getItem('manageDormID')
      const roomId = this.roomId
      let success = true
      for (const file of this.uploadFiles) {
        const formData = new FormData()
        if (this.validate(file) === '') {
          formData.set('uploaded_photo', file)
          await this.uploadFile(dormId, roomId, formData).then(() => {
            this.files.shift()
          }).catch(() => {
            success = false
          }).then(() => {
            this.loadingBtn = false
          })
        }
      }
      if (success) {
        this.resetFiles()
        this.$store.dispatch('fetchManagerDormRooms', dormId)
        let snackbar = {
          message: this.lang.snackbar.successRoomEdit,
          color: 'success'
        }
        this.closeEditDialog()
        setTimeout(() => {
          this.$store.commit('updateSnackbar', snackbar)
        }, 700)
      }
    },
    clean(data) {
      Object.keys(data).forEach((key) => (data[key] == null || data[key].length == 0) && delete data[key]);
    },
    submitChanges() {
      const dormId = localStorage.getItem('manageDormID')
      const roomId = this.roomId
      let getRadioArray = this.roomFilters.radioChoices.map(radioChoices => radioChoices.selected_number);
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
      if (this.$refs.form.validate()) {
        this.loadingBtn = true
        this.clean(roomData)
        this.$backend.$updateRoomData(dormId, roomId, roomData).then(() => {
          this.submitPhotos()
        }).catch((err) => {
          let snackbar
          if (err.response.status == 403 || err.response.status == 500) {
            snackbar = {
              message: this.lang.snackbar.wrongMsg,
              color: 'error'
            }
            this.$store.commit('updateSnackbar', snackbar)
          } else {
            snackbar = {
              message: err,
              color: 'error'
            }
            this.$store.commit('updateSnackbar', snackbar)
          }
        }).then(() => {
          this.loadingBtn = false
        })
      }
    },
    selectNewFile() {
      const files = this.$refs.editRoomfiles.files
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
    validate(file) {
      const MAX_SIZE = 8000000
      const allowedType = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
      if (file.size > MAX_SIZE) {
        return `${this.confirmPayment.fileMaxSize}: ${MAX_SIZE / 1000}KB`
      }
      if (!allowedType.includes(file.type)) {
        return this.confirmPayment.notAllowedType
      }
      return ''
    },
    isValid() {
      for (var file of this.uploadFiles) {
        if (this.validate(file) != '') {
          this.btnDisabled = true
          break;
        }
        this.btnDisabled = false
      }
      if (!this.uploadFiles.length) {
        this.btnDisabled = false
      }
    },
    removeFile(index) {
      this.files.splice(index, 1)
      this.uploadFiles.splice(index, 1)
      this.isValid()
    },
    resetFiles() {
      this.files = []
      this.uploadFiles = []
    },
    addFilter(filterId, optionId, type) {
      let filtersArray
      if (type == 'radio') {
        filtersArray = this.roomFilters.radioChoices
      } else {
        filtersArray = this.roomFilters.integralChoices
      }
      let objectUpdated = 0;
      for (const filter of filtersArray) {
        if (filter.id == filterId) {
          filter.selected_number = optionId
          objectUpdated = -1;
          continue;
        }
      }
      if (objectUpdated == 0) {
        filtersArray.push({
          id: filterId,
          selected_number: optionId
        })
      }
    },
    confirmDelete(id) {
      this.deletePhoto.id = id
      this.deletePhoto.confirmDialog = true
    },
    deleteRoomPhoto() {
      const dormId = localStorage.getItem('manageDormID')
      const roomId = this.roomId
      const photoId = this.deletePhoto.id
      this.$backend.$deleteRoomPhoto(dormId, roomId, photoId).then(() => {
        this.deletePhoto.confirmDialog = false
        return this.$backend.$fetchEditRoomFilters(dormId, roomId)
      }).then((response) => {
        this.roomData = response
      }).catch((err) => {
        let snackbar = {
          message: err,
          color: 'error'
        }
        this.$store.commit('updateSnackbar', snackbar)
      })
    }
  },
  watch: {
    isUpdating(val) {
      if (val) {
        setTimeout(() => (this.isUpdating = false), 3000)
      }
    }
  }
};