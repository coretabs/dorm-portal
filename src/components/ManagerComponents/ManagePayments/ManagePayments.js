
export default {
  name: "ManagePayments",
  data: function () {
    return {
      showDetails: false,
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
      reservations: [
        {
          id: 1,
          amount: 1600,
          name: 'Mohammed Alhakem',
          passport: '05727780',
          email: 'Alhakeem.prof@gmail.com',
          submittedOn: '2/2/2018',
          deadline: '4/2/2018',
          status: 'pending',
          receipts: ['https://google.com'],
          room_type: 'Singel Room',
          duration: 'summer'
        },
        {
          id: 2,
          amount: 1000,
          name: 'Yasser Alnajjar',
          passport: '05727780',
          email: 'Alhakeem.prof@gmail.com',
          submittedOn: '2/2/2018',
          deadline: '4/2/2018',
          status: 'confirmed',
          receipts: ['https://google.com','https://youtube.com'],
          room_type: 'Double Room',
          duration: 'full Academic Year'
        },
        {
          id: 3,
          amount: 3000,
          name: 'Yasser Alnajjar',
          passport: '05727780',
          email: 'Alhakeem.pro@gmail.com',
          submittedOn: '2/2/2018',
          deadline: '4/2/2018',
          status: 'Unpaid',
          receipts: ['https://google.com','https://youtube.com'],
          room_type: 'Singel Room',
          duration: 'summer'
        },
        {
          id: 4,
          amount: 4000,
          name: 'Yasser Alnajjar',
          passport: '05727780',
          email: 'Alhakeem.prof@gmail.com',
          submittedOn: '2/2/2018',
          deadline: '4/2/2018',
          status: 'confirmed',
          receipts: ['https://google.com','https://youtube.com'],
          room_type: 'Dalux Room',
          duration: 'fall'
        }
      ],
      details:{
        name: '',
        roomType: '',
        duration:''

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
      this.details.duration = item.duration
      this.details.roomType =  item.room_type
    }
  },
  mounted(){
    this.setHeaderText()
  }
};