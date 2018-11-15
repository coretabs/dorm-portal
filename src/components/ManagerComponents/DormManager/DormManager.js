
import ManageDorm from '../ManageDorm/ManageDorm.vue'

export default {
  name: "DormManager",
  components: {
    ManageDorm
  },
  data: function () {
    return {
      drawerControl: null,
      currentTabComponent: ManageDorm,
      drawerMenu: [
        {
          icon: 'fa-chart-line',
          componentName : 'DashboardComponent'
        },
        {
          icon: 'fa-building',
          componentName : 'ManageDorm'
        },
        {
          icon: 'fa-bed',
          componentName : 'RoomsComponent'
        },
        {
          icon: 'fa-money-bill-wave',
          componentName : 'PaymentsComponent'
        },
        {
          icon: 'fa-users',
          componentName : 'StudentsComponent'
        }
      ]
    };
  },
  methods: {
    loadComponent(component){
      this.currentTabComponent = component
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }    
  }
};