export default {
  name: "DormSearch",
  props:{
    'dutarion': Array,
    'category': Array
  },
  data: function () {
    return {
      chosenDutarion: null,
      chosenCategory: null,
      loading: false
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    defaultDormType(){
      if(this.category != null){
        return this.category[0].name
      }
    },
    defaultAcademicYear(){
      if(this.dutarion != null){
        return this.dutarion[0].name
      }
    }
  },
  methods: {
    search(){
      this.loading = true
      this.$store.state.userFilters.category = this.chosenCategory
      this.$store.state.userFilters.duration = this.chosenDutarion
      let data = {
        lang: this.$store.state.language,
        currency: this.$store.state.currencyCode,
        duration: this.chosenDutarion,
        category: this.chosenCategory,
        dormFeatures: this.$store.state.userFilters.dorm_features,
        roomFeatures: this.$store.state.userFilters.room_features,
        additionalFilters: this.$store.state.userFilters.additional_filters
      }
      this.$store.dispatch('fetchSearchedDorms', data).then(()=>{
        this.loading = false
        this.$emit('showResultAlert', true)
      })
    }
  }
};