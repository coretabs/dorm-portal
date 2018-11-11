export default {
  name: "DormSearch",
  data: function () {
    return {
      number: 5,
      DormsType: ["All Dorms", "EMU Dorms", "Private Dorms"],
      AcademicYear: ["Academic year", "Spring", "Fall", "Summer"],
      defaultDormType: "All Dorms",
      defaultAcademicYear: "Academic year"
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  }
};