export default {
  name: "DormSearch",
  props:{
    'dutarion': Object,
    'category': Object
  },
  data: function () {
    return {
      number: 5,
      DormsType: this.category,
      AcademicYear: this.dutarion,
      defaultDormType: "EMU Dorms",
      defaultAcademicYear: "Academic year"
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  }
};