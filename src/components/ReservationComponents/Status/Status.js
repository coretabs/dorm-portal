export default {
  name: 'Status',
  data: function(){
    return{
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
    }
  }
};