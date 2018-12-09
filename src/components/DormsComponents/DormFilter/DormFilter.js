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
    };
  },
  methods: {

    fetchFilters() {
      this.$store.dispatch('fetchFilters');
    },

    fetchDorms() {
      this.$store.dispatch('fetchDorms');
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
      return this.$store.state.filters[0].duration_options
    },
    setCategory(){
      return this.$store.state.filters[0].category_options
    }
  },
  mounted() {
    this.fetchFilters();
    this.fetchDorms();
  }
};