
import ManageDorm from '../ManageDorm/ManageDorm.vue'
import ManageRooms from '../ManageRooms/ManageRooms.vue'
import ManageReservations from '../ManageReservations/ManageReservations.vue'
import AddNewRoom from '../AddNewRoom/AddNewRoom.vue'
import SelectDorm from '../SelectDorm/SelectDorm.vue'

export default {
  name: "DormManager",
  components: {
    ManageDorm,
    ManageRooms,
    ManageReservations,
    AddNewRoom,
    SelectDorm
  },
  data: function () {
    return {
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
      this.$store.state.adminActiveComponent = component
    },
    fetchManagerDorms(){
      this.$store.dispatch("fetchManagerDorms").then((response)=>{
        if(response.length > 1 && !localStorage.getItem("manageDormID")){
          this.$store.state.drawer = false
          this.$store.state.adminActiveComponent = 'SelectDorm'
        }else{
          this.$store.state.drawer = null
          this.$store.state.adminActiveComponent = 'ManageReservations'
        }
      })
    },
    checkAuth(){
      if(this.$store.getters.isLoggedIn){
        this.$store.dispatch('auth')
        .catch(() => {
          this.$store.dispatch('logout')
          .then(() => {
            this.$router.push('/login')
          })
        })
     }
    },
  },
  computed: {
    lang() {
      return this.$store.getters.lang
    },
    currentTabComponent(){
      return this.$store.getters.adminActiveComponent
    },
    drawerControl(){
      return this.$store.getters.drawer
    }
  },
  created() {
  },
  mounted(){
    this.checkAuth()
    this.$root.$on('currentTabComponent',(componentName) => {
      this.$store.state.adminActiveComponent = componentName;
    })
    this.fetchManagerDorms()
  }
};