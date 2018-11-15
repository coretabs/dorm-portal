
const srcs = {
  1: 'https://cdn.vuetifyjs.com/images/lists/1.jpg',
  2: 'https://cdn.vuetifyjs.com/images/lists/2.jpg',
  3: 'https://cdn.vuetifyjs.com/images/lists/3.jpg',
  4: 'https://cdn.vuetifyjs.com/images/lists/4.jpg',
  5: 'https://cdn.vuetifyjs.com/images/lists/5.jpg'
}
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