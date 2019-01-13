import DormCard from "../DormCard/DormCard.vue";
import DormSearch from "../DormSearch/DormSearch.vue";
export default {
  name: "DormFilter",
    components: {
    "dorm-card": DormCard,
    "dorm-search": DormSearch
  },
  data: function () {
    return {
      showAlert: false,
      dormSelectedFeatures: [],
      roomSelectedFeatures: [],
      roomIntegralFilters:[],
      additionalFiltersHolder:[],
      optionsHolder: [],
      minValue: null,
      loadingFilters: false,
      loadingDorms: false
    };
  },
  watch: {
    lang() {
      this.updatedLocaleFetching()
    },
    activeCurrency(){
      this.updatedLocaleFetching()
    }
  },
  methods: {
    fetchFilters() {
      this.loadingFilters = true
      this.$store.dispatch('fetchFilters', this.activeCurrency).then(()=>{
        this.loadingFilters = false
      })
    },
    fetchDorms() {
      this.$store.dispatch('fetchDorms')
    },
    dormFeatiresFilter(){
      this.$store.state.userFilters.dorm_features = this.dormSelectedFeatures
      this.dispatchFilter()
    },
    roomFeatiresFilter(){
      this.$store.state.userFilters.room_features = this.roomSelectedFeatures
      this.dispatchFilter()
    },
    selectedAdditionalFilters(filterID, optionID){
      let objectUpdated = 0;
      for(const filter of this.roomIntegralFilters){
        if (filter.id === filterID){
          let optionsArray = filter.choosen_options_ids
          if(optionsArray.includes(optionID)){
            let index = optionsArray.indexOf(optionID)
            optionsArray.splice(index, 1)
            objectUpdated = -1;
            continue;
          }else{
            optionsArray.push(optionID)
            objectUpdated = -1;
            continue;
          }
        }
      }
      if(objectUpdated != -1){
        this.optionsHolder.push(optionID)
        this.$store.state.userFilters.additional_filters.push({
          id: filterID,
          choosen_options_ids: this.optionsHolder
        })
        this.optionsHolder = []
      }
      this.roomIntegralFilters = this.$store.state.userFilters.additional_filters
      this.dispatchFilter()
    },
    integralFilter(value, id){
      const minValue = value[0]
      const maxValue = value[1]
      let objectUpdated = 0;
      for(const filter of this.roomIntegralFilters){
        if (filter.id === id) {
          filter.min_value = minValue;
          filter.max_value = maxValue;
          objectUpdated = -1;
          continue;
        }
      }
      if(objectUpdated != -1){
        this.$store.state.userFilters.additional_filters.push({
          id: id,
          min_value: minValue,
          max_value: maxValue
        })
        this.roomIntegralFilters = this.$store.state.userFilters.additional_filters
       }
       this.dispatchFilter()
    },
    dispatchFilter(){
      this.loadingDorms = true
      let data = {
        lang: this.$store.state.language,
        currency: this.$store.state.currencyCode,
        duration: this.$store.state.userFilters.duration,
        category: this.$store.state.userFilters.category,
        dormFeatures: this.$store.state.userFilters.dorm_features,
        roomFeatures: this.$store.state.userFilters.room_features,
        additionalFilters: this.$store.state.userFilters.additional_filters
      }
      this.$store.dispatch('fetchSearchedDorms', data).then(()=>{
        this.loadingDorms = false
        this.showAlert = true
      })
    },
    updatedLocaleFetching(){
      this.fetchFilters()
      this.dispatchFilter()
    },
    showResultAlert(status){
      this.showAlert = status
    }
  },
  computed: {
    lang(){
      return this.$store.getters.lang;
    },
    activeCurrency(){
      return this.$store.state.currencyCode
    },
    drawerControl(){
      return this.$store.state.drawer;
    },
    filters(){
      return this.$store.state.filters;
    },
    dorms(){
      return this.$store.state.dorms;
    },
    setDuration(){
      let allTime = {
        name: this.lang.dormSearch.allTime,
        id: null
      }
      const duration = this.$store.state.filters.duration_options
      if(duration){
        duration.push(allTime)
      }
      return duration
    },
    setCategory(){
      let allDorms = {
        name: this.lang.dormSearch.allDorms,
        id: null
      }
      const category = this.$store.state.filters.category_options
      if(category){
        category.push(allDorms)
      }
      return category
    },
    resultAlert(){
      return this.$store.state.dorms.length
    }
  },
  mounted() {
    this.fetchFilters();
    this.fetchDorms();
  }
};