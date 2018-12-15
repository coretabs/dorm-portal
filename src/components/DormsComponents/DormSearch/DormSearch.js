export default {
  name: "DormSearch",
  props:{
    'dutarion': Array,
    'category': Array
  },
  data: function () {
    return {
      number: 5,
      defaultAcademicYear: "Academic year"
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    defaultDormType(){
      if(this.category != null){
        return this.category[0].name
      }
    },
    defaultAcademicYear(){
      if(this.dutarion != null){
        return this.dutarion[0].name
      }
    }
  }
};