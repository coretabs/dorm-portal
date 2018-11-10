<template>
  <v-form id="search-dorm">
    <h2>{{lang.dormSearch.heading}}</h2>
    <v-layout row wrap>
      <v-flex xs12 sm3>
        <v-select
          :items="DormsType"
          label="Dormitories type"
          prepend-inner-icon="meeting_room"
          solo color="success"
          append-icon="expand_more" 
          :menu-props="{
            offsetY: '',
            transition: 'slide-y-transition',
            bottom: ''
          }"
          v-model="defaultDormType"
        ></v-select>
      </v-flex>
      <v-flex xs12 sm2>
        <v-select class="shift-left"
          :items="AcademicYear"
          label="Duration"
          prepend-inner-icon="calendar_today"
          solo color="success"
          append-icon="expand_more" 
          :menu-props="{
            offsetY: '',
            transition: 'slide-y-transition',
            bottom: ''
          }"
          v-model="defaultAcademicYear"
        ></v-select>
      </v-flex>
      <v-flex xs12 md1>
        <v-btn depressed large><v-icon>fa-search</v-icon>{{lang.dormSearch.button}}</v-btn>
      </v-flex>
    </v-layout>
  </v-form>
</template>

<script>
  export default {
    name: 'DormSearch',
    data: function (){
      return{
        number: 5,
        DormsType: ['All Dorms', 'EMU Dorms', 'Private Dorms'],
        AcademicYear: ['Academic year', 'Spring', 'Fall', 'Summer'],
        defaultDormType: 'All Dorms',
        defaultAcademicYear: 'Academic year',
      }
    },
    computed: {
      lang(){ return this.$store.getters.lang }
    }
  }
</script>

<style lang="scss">
@import '../../assets/styles/vars';
@import '../../assets/styles/mixins';
#search-dorm{
  margin-bottom: 20px;
  h2{
    margin: 0px 0 20px;
  }
  .flex{
    padding: 0px;
  }
  .v-input__slot{
    box-shadow: none;
    border: 1px solid #ccc;
  }
  .shift-left .v-input__slot{
    margin-left: -2px;
  }
  .v-input__prepend-inner{
    margin-right: 10px;
    .v-icon{
      color: #ccc;
      font-size: 20px;
    }
  }
  .v-btn--large{
    margin: 0;
    background: #feae25;
    padding: 0;
    height: 48px;
    width: 100%;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
    margin-left: -3px;
    -webkit-box-shadow:inset 0px 0px 0px 1px #ccc;
    -moz-box-shadow:inset 0px 0px 0px 1px #ccc;
    box-shadow:inset 0px 0px 0px 1px #ccc;
    .v-icon{
      font-size: 14px;
      margin-right: 6px; 
    }
  }
}
</style>