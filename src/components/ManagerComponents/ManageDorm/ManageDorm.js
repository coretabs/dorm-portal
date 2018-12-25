import FileUpload from 'vue-upload-component/src'

export default {
  name: "ManageDorm",
  components: {
    'file-upload': FileUpload
  },
  data: function () {
    return {
      active: null,
      items: ['Streaming', 'Eating'],
      selectedFeatures: [1,2],
      selectedFeaturesId: [],
      isUpdating: false,
      loadingBtn: false,
      Features: [
        { name: 'Free wifi', id: 1},
        { name: 'Free parking', id: 2},
        { name: 'Hot water', id: 3},
        { name: 'Cold water', id: 4}
      ],
      files: [],
      dialog: {
        general: false
      },
      dormsAboutDesc:[1,2],
      requiredRules:[
        v => !!v || 'This field is required'
      ],
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    languages(){
      return this.$store.state.languages;
    },
    currencies(){
      return this.$store.state.currencies;
    },
    dorm(){
      return this.$store.getters.manageDorm
    }
  },
  methods: {
    remove (item) {
      const index = this.selectedFeatures.indexOf(item.id)
      if (index >= 0) this.selectedFeatures.splice(index, 1)
    },
    fetchManagerDorm(){
      const dormID = localStorage.getItem('manageDormID')
      this.$store.dispatch("fetchManagerDorm", dormID)
      .catch(()=>{
        this.$store.state.snackbar.trigger = true
        this.$store.state.snackbar.message = 'Can\'t load dorm'
        this.$store.state.snackbar.color = 'error'
      })
    },
    updateDialog(dialogName){
      this.dialog[dialogName] = true
    },
    closeDialog(dialogName){
      const dormID = localStorage.getItem('manageDormID')
      this.dialog[dialogName] = false
      this.$store.dispatch("fetchManagerDorm", dormID)
    },
    submitDormInfo(){
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
        contact_email: this.dorm.contact_email
      }
      if(this.$refs.form.validate()){
        this.loadingBtn = true
        this.$store.dispatch("updateDormInfo", data).then(()=>{
          let snackbar = {
            message: 'Updeated successfully',
            color: 'success'
          }
          this.closeDialog('general')
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