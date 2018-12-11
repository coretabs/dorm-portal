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
      switch(this.$store.state.reservation.status){
        case 1:
          this.status = "Confirmed"
          this.statusIcon = "fa-check"
          break;
        case 2:
          this.status = "Updated"
          this.statusIcon = "fa-clock"
          break;
        case 3:
          this.status = "rejected"
          this.statusIcon = "fa-times"
          break;
        default:
          this.status = "Pending"
          break;
      }
      return this.$store.state.reservation;
    }
  }
};