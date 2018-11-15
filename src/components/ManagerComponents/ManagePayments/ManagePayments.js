
export default {
  name: "ManagePayments",
  data: function () {
    return {
      search: '',
        headers: [
          { text: 'Amount', value: 'amount' },
          { text: 'Student Name', value: 'name' },
          { text: 'Student Email', value: 'email' },
          { text: 'Submitted On', value: 'submittedOn' },
          { text: 'Deadline', value: 'deadline' },
          { text: 'Status', value: 'status' },
          { text: 'Receipts', value: 'receipts' },
          { text: 'Actions', value: 'id', sortable: false }
        ],
        payments: [
          {
            id: 1,
            amount: 1600,
            name: 'Mohammed Alhakem',
            email: 'Alhakeem.prof@gmail.com',
            submittedOn: '2/2/2018',
            deadline: '4/2/2018',
            status: 'Pending',
            receipts: ['https://google.com','https://youtube.com']
          },
          {
            id: 2,
            amount: 1600,
            name: 'Yasser Alnajjar',
            email: 'Alhakeem.prof@gmail.com',
            submittedOn: '2/2/2018',
            deadline: '4/2/2018',
            status: 'Pending',
            receipts: ['https://google.com','https://youtube.com']
          }
        ]
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }    
  },
  methods: {
   
  }
};