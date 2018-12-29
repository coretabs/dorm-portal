import FileUpload from 'vue-upload-component/src'

export default {
  name: "ManageDorm",
  components: {
    'file-upload': FileUpload
  },
  data: function () {
    return {
      selectedFeatures:[],
      files: [],
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
      }
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
      if(objectUpdated != -1){
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
        this.$store.dispatch('addNewRoom', {dormID,roomData}).then(()=>{
          console.log('done')
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
    this.fetchRoomFilters()
  }
};