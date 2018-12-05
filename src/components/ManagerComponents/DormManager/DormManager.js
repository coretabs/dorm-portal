
import ManageDorm from '../ManageDorm/ManageDorm.vue'
import ManageRooms from '../ManageRooms/ManageRooms.vue'
import ManageReservations from '../ManageReservations/ManageReservations.vue'
import AddNewRoom from '../AddNewRoom/AddNewRoom.vue'

export default {
  name: "DormManager",
  components: {
    ManageDorm,
    ManageRooms,
    ManageReservations,
    AddNewRoom
  },
  data: function () {
    return {
      drawerControl: null,
      currentTabComponent: ManageDorm,
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
  },
  created() {
    this.$root.$on('currentTabComponent',(componentName) => {
      this.currentTabComponent = componentName;
    })
  }
};