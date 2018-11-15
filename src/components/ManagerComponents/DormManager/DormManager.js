
import ManagerDashboard from '../ManagerDashboard/ManagerDashboard.vue'
import ManageDorm from '../ManageDorm/ManageDorm.vue'
import ManageRooms from '../ManageRooms/ManageRooms.vue'
import ManagePayments from '../ManagePayments/ManagePayments.vue'
import ManageStudents from '../ManageStudents/ManageStudents.vue'

export default {
  name: "DormManager",
  components: {
    ManageDorm,
    ManageRooms,
    ManagePayments,
    ManageStudents,
    ManagerDashboard
  },
  data: function () {
    return {
      drawerControl: null,
      currentTabComponent: ManagePayments,
      drawerMenu: [
        {
          icon: 'fa-chart-line',
          componentName : 'ManagerDashboard'
        },
        {
          icon: 'fa-building',
          componentName : 'ManageDorm'
        },
        {
          icon: 'fa-bed',
          componentName : 'ManageRooms'
        },
        {
          icon: 'fa-money-bill-wave',
          componentName : 'ManagePayments'
        },
        {
          icon: 'fa-users',
          componentName : 'ManageStudents'
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