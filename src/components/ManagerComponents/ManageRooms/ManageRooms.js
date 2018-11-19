
export default {
  name: "ManageRooms",
  data: function () {
    return {
      quota: 5,
      showQuotaUpdate: false,
      items: [
        { title: 'Edit' },
        { title: 'Delete' }
      ]
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }    
  },
  methods:{
    loadComponent(componentName){
      this.$root.$emit('currentTabComponent', componentName)
    }
  }
};