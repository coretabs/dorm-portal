
import EditRoom from '../EditRoom/EditRoom.vue'
import _ from 'lodash'

export default {
  name: "ManageRooms",
  components:{
    EditRoom
  },
  data: function () {
    return {
      showQuotaUpdatedialog: false,
      showRoomDetailsdialog: false,
      showEditRoomDialog: false,
      deleteDialog:{
        show: false,
        roomId: null
      },
      loadingBtn: false,
      quotaRoomID: null,
      roomEditId: null,
      roomDetails: {},
      items: [
        { title: 'Edit' },
        { title: 'Delete' }
      ]
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    rooms(){
      return _.reverse(_.orderBy(this.$store.getters.managerDormRooms, 'id', ['asn']))
    }
  },
  methods:{
    loadComponent(componentName){
      this.$root.$emit('currentTabComponent', componentName)
    },
    showRoomDetails(room){
      this.roomDetails = room;
      this.showRoomDetailsdialog = true
    },
    showQuotaUpdate(reservedRooms, totalRooms, allowedQuota, roomID){
      this.reservedRoomsNumber = reservedRooms
      this.totalRoomsNumber = totalRooms
      this.allowedQuotaNumber = allowedQuota
      this.quotaRoomID = roomID
      this.showQuotaUpdatedialog = true
    },
    UpdateQuotaNumber(){
      let snackbar
      if(this.allowedQuotaNumber <= this.availableRoomsNumber){
        let roomData = {
          allowedQuota: this.allowedQuotaNumber
        }
        const roomId = this.quotaRoomID
        const dormId = localStorage.getItem('manageDormID')
        this.$store.dispatch('updateRoomData', {dormId, roomId, roomData}).then(()=>{
          snackbar = {
            message: 'ٌRoom Quota Has been Updated Successfully',
            color: 'success'
          }
          this.$store.dispatch('fetchManagerDormRooms',dormId)
          this.showQuotaUpdatedialog = false
        }).catch(()=>{
          snackbar = {
            message: 'Some thing went wrong! try again',
            color: 'error'
          }
        }).then(()=>{
          this.$store.commit('updateSnackbar', snackbar)
        })
      }else{
        snackbar = {
          message: 'You have only ' + this.availableRoomsNumber + ' room avaliable',
          color: 'error'
        }
        this.$store.commit('updateSnackbar', snackbar)
      }
    },
    progressValue(reserved_rooms,total_rooms){
      return reserved_rooms / total_rooms * 100;
    },
    availableRooms(reservedRooms, totalRooms){
      this.availableRoomsNumber = totalRooms - reservedRooms;
      return this.availableRoomsNumber;
    },
    countAvailableRooms(reservedRooms,totalRooms){
      return totalRooms - reservedRooms;
    },
    progressColor(allowedQuota, totalRooms, reservedRooms){
      return (allowedQuota >= 5) ? "#39c463" : ( totalRooms-reservedRooms == 0) ? "#39c463" : "#cf5151";
    },
    quotaTextColor(quota, totalRooms, reservedRooms){
      return (quota < 5 && totalRooms-reservedRooms > quota ) ? "red--text" : "black--text";
    },
    editRoom(roomId){
      this.fetchEditRoomFilters(roomId)
      this.showEditRoomDialog = true;
    },
    deleteRoom(roomId){
      this.deleteDialog.show = true
      this.deleteDialog.roomId = roomId
    },
    confirmDeleteRoom(){
      const dormId = localStorage.getItem('manageDormID')
      const roomId = this.deleteDialog.roomId
      this.loadingBtn = true
      let snackbar
      this.$store.dispatch('deleteDormRoom',{dormId,roomId}).then(()=>{
        snackbar = {
          message: 'Room has been deleted successfully',
          color: 'success'
        }
        this.fetchManagerDormRooms()
        this.deleteDialog.show = false
      }).catch(()=>{
        snackbar = {
          message: 'Something went wrong! try again',
          color: 'error'
        }
      }).then(()=>{
        this.$store.commit('updateSnackbar', snackbar)
        this.loadingBtn = false
      })
    },
    fetchManagerDormRooms(){
      const dormID = localStorage.getItem('manageDormID')
      this.$store.dispatch('fetchManagerDormRooms',dormID)
    },
    fetchEditRoomFilters(roomId){
      const dormId = localStorage.getItem('manageDormID')
      this.$store.dispatch('fetchEditRoomFilters', {dormId, roomId}).then((response)=>{
        this.roomEditId = roomId
        this.roomDetails = response
      })
    },
    closeEditDialog(dialogStatus){
      this.showEditRoomDialog = dialogStatus
    },
    updateRoomStatus(roomId, roomStatus){
      let roomData = {
        isReady: roomStatus
      }
      const dormId = localStorage.getItem('manageDormID')
      this.$store.dispatch('updateRoomData', {dormId, roomId, roomData}).then(()=>{
        let snackbar = {
          message: 'ٌRoom Status Has been Updated Successfully',
          color: 'success'
        }
        this.$store.commit('updateSnackbar', snackbar)
        this.$store.dispatch('fetchManagerDormRooms',dormId)
      }).catch(()=>{
        let snackbar = {
          message: 'Some thing went wrong! try again',
          color: 'error'
        }
        this.$store.commit('updateSnackbar', snackbar)
      })
    }
  },
  mounted(){
    this.fetchManagerDormRooms()
  }
};