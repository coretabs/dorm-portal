
import ManageDorm from '../ManageDorm/ManageDorm.vue'
import ManageRooms from '../ManageRooms/ManageRooms.vue'
import ManageReservations from '../ManageReservations/ManageReservations.vue'

export default {
  name: "DormManager",
  components: {
    ManageDorm,
    ManageRooms,
    ManageReservations,
  },
  data: function () {
    return {
      drawerControl: null,
      currentTabComponent: ManageRooms,
      drawerMenu: [
        {
          icon: 'fa-money-bill-wave',
          componentName : 'ManageReservations'
        },
        {
          icon: 'fa-bed',
          componentName : 'ManageRooms'
        },
        {
          icon: 'fa-building',
          componentName : 'ManageDorm'
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