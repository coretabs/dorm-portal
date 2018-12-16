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
      showAlert: true,
      dormSelectedFeatures: [],
      roomSelectedFeatures: []
    };
  },
  methods: {

    fetchFilters() {
      this.$store.dispatch('fetchFilters');
    },

    // fetchDorms() {
    //   this.$store.dispatch('fetchDorms');
    // },
    dormFeatiresFilter(){
      this.$store.state.userFilters.dorm_features = this.dormSelectedFeatures
      this.$store.dispatch('fetchSearchedDorms')
    },
    roomFeatiresFilter(){
      this.$store.state.userFilters.room_features = this.roomSelectedFeatures
      this.$store.dispatch('fetchSearchedDorms')
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
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
        name: 'All Time',
        id: null
      }
      this.$store.state.filters.duration_options.push(allTime)
      return this.$store.state.filters.duration_options
    },
    setCategory(){
      let allDorms = {
        name: 'All dormitories',
        id: null
      }
      this.$store.state.filters.category_options.push(allDorms)
      return this.$store.state.filters.category_options
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