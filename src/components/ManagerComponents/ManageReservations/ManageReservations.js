
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
      status: this.$store.getters.lang.manageResrevations.status,
      currentStatus: '',
      followUpMessage: '',
      reservationID: null,
      statusIndex: null,
      details:{
        roomType: '',
        duration:'',
        people: null
      },
      messageRules:[
        v => !!v || 'Message is required',
        v => v.length >= 6 || 'Message Must be more than 8 letters'
      ],
      statusRules:[
        v => !!v || 'Status is required',
      ],
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    reservations(){
      return this.$store.getters.manageReservation;
    },
    showDate(){

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
      //this.date = item.confirmation_deadline_date
      this.reservationID = item.id
    },
    close(){
      this.showUpdateStatus = false,
      this.currentStatus = '',
      this.followUpMessage = ''
    },
    fetchManagerReservation(){
      let dorm = this.$store.getters.managerDorms
      if(dorm){
        dorm = dorm[0].id
      }
      const dormID = localStorage.getItem('manageDormID') ||  dorm
      this.$store.dispatch("fetchManagerReservation", dormID)
    },
    setStatusIndex(){
      this.statusIndex = this.status.indexOf(this.currentStatus)
    },
    submit(){
 
      let data = {
        reservationID: this.reservationID,
        dormID: localStorage.getItem('manageDormID'),
        status: this.statusIndex,
        deadline: this.date,
        message: this.followUpMessage
      }
      if(this.$refs.form.validate()){
        this.$store.dispatch("updateReservationStatus", data)
      }
    },
  },
  mounted(){
    this.fetchManagerReservation(),
    this.setHeaderText()
  }
};