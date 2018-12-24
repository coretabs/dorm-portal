
export default {
  name: "ManageReservations",
  data: function () {
    return {
      showDetails: false,
      showUpdateStatus: false,
      date: null,
      menu: false,
      search: '',
      headers: [
        { text: '', value: 'amount' },
        { text: '', value: 'receipts', sortable: false  },
        { text: '', value: 'status' },
        { text: '', value: 'name' },
        { text: '', value: 'email' },
        { text: '', value: 'submittedOn' },
        { text: '', value: 'deadline' },
        { text: '', value: 'id', sortable: false }
      ],
      reservations: [],
      status: [
        'confirmed',
        'pending',
        'Rejected',
        'Unpaid'
      ],
      currentStatus: '',
      currentStatusId: null,
      details:{
        roomType: '',
        duration:'',
        people: null
      }
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  },
  methods:{
    setHeaderText(){
      let arrLength = this.lang.manageResrevations.tableHeaders.length
      for(var i=0 ; i <= arrLength ; i++)
        this.headers[i].text = this.lang.manageResrevations.tableHeaders[i]
    },
    filterStatus(keyWord){
      this.search = keyWord
    },
    showMoreDetails(item){
      this.showDetails = true
      this.details.duration = item.room_characteristics.duration
      this.details.roomType =  item.room_characteristics.room_type
      this.details.people = item.room_characteristics.people_allowed_number
    },
    updateStatus(item){
      this.showUpdateStatus = true
      this.date = item.deadline
      this.currentStatusId = item.id
      this.currentStatus = item.status
    },
    fetchManagerReservation(){
      let dorm = this.$store.getters.managerDorms
      if(dorm){
        dorm = dorm[0].id
      }
      const dormID = localStorage.getItem('manageDormID') ||  dorm
      this.$store.dispatch("fetchManagerReservation", dormID).then((response)=>{
        this.reservations = response
      })
    }
  },
  mounted(){
    this.fetchManagerReservation(),
    this.setHeaderText()
  }
};