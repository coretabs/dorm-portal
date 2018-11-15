export default {
  name: "ManageDorm",
  data: function () {
    return {
      active: null,
      dormName: 'Alfam Dorm',
      items: ['Streaming', 'Eating'],
      selectedFeatures: [1,2],
      selectedFeaturesId: [],
      isUpdating: false,
      Features: [
        { name: 'Free wifi', id: 1},
        { name: 'Free parking', id: 2},
        { name: 'Hot water', id: 3},
        { name: 'Cold water', id: 4}
      ]
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
    }
  },
  methods: {
    remove (item) {
      const index = this.selectedFeatures.indexOf(item.id)
      if (index >= 0) this.selectedFeatures.splice(index, 1)
    }
  },
  watch: {
    isUpdating (val) {
      if (val) {
        setTimeout(() => (this.isUpdating = false), 3000)
      }
    }
  },
};