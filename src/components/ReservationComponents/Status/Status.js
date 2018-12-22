export default {
  name: 'Status',
  data: function(){
    return{
      status: "",
      statusIcon: "",
      items: [{
        iconClass: 'grey lighten-1 white--text',
        title: 'Receipt01',
        subtitle: 'Jan 9, 2014'
        },
        {
          iconClass: 'grey lighten-1 white--text',
          title: 'Receipt02',
          subtitle: 'Jan 17, 2014'
        },
        {
          iconClass: 'grey lighten-1 white--text',
          title: 'Receipt03',
          subtitle: 'Jan 28, 2014'
        }
      ]
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    reservation(){
      switch(this.$store.getters.reservationData.status){
        case '0':
          this.status = "pending"
          break;
        case '1':
          this.status = "rejected"
          this.statusIcon = "fa-times"
          break;
        case '2':
          this.status = "confirmed"
          this.statusIcon = "fa-check"
          break;
          case '3':
          this.status = "Wating"
          this.statusIcon = "fa-clock"
          break;
        case '4':
          this.status = "Updated"
          this.statusIcon = "fa-bell"
          break;
        case '5':
          this.status = "Expired"
          this.statusIcon = "fa-times"
          break;
        default:
          this.status = "Unknown"
          break;
      }
      return this.$store.getters.reservationData
    }
  }
};