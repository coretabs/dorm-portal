<template>

  <div id="filter">

    <!-- filters sidebar -->
    <v-navigation-drawer
      :clipped="$vuetify.breakpoint.lgAndUp"
      v-model="drawer" fixed app>
      <template>
        <div id="filters-heading"><v-icon left>filter_list</v-icon> {{filtersHeading}}</div>
        <div id="filters-body">
          <div class="filter" v-for= "(filter,index) in filters" :key="index">
            <div class="filter-title">{{filter.title}}</div>
            <ul>
              <li v-for= "(option, index) in filter.options" :key="index">
                <v-checkbox v-model="checkboxs" :value="option" :label="option" color="success"></v-checkbox>
              </li>
            </ul>
          </div>
        </div> 
      </template>
    </v-navigation-drawer>

    <!-- Filtered dorms -->
    <v-content>
      <v-container id="rightside" fluid>
        <v-layout row wrap>

            <!-- search form -->
            <v-flex xs12>
              <dorm-search></dorm-search>
            </v-flex>

            <!-- number of result -->
            <!-- <v-flex xs12>
              <v-alert :value="true" type="success" >
                {{successSearch}}
              </v-alert>
               <v-alert :value="true" type="error" >
                {{successSearch}}
              </v-alert> 
            </v-flex>-->

            <!-- dorms card -->
            <v-flex xs12>
              <dorm-card v-for="n in 5" :key="n"></dorm-card>
            </v-flex>
          
        </v-layout>
      </v-container>
    </v-content>

  </div>

</template>

<script>
  import DormCard from './DormCard'
  import DormSearch from './DormSearch'
  export default {
    name: 'DormFilter',
    components: {
      'dorm-card' :DormCard,
      'dorm-search': DormSearch
    },
    data: function (){
      return{
        drawer: null,
        filtersHeading: 'Filter by:',
        filters: [
          {
            title: 'Availabilty',
            options: ['show only available dorms', "show all dorms"]
          },
          {
            title: "Discount Opportunity",
            options: ["Discounted dorms"]
          },
          {
            title: "Meals",
            options: ["3 Meals included", "Breakfast included", "Dinner included"]
          },
          {
            title: "Shopping Opportunity",
            options: ["Restorant / Cafeteria", "Hairdresser / Barber", "Market"]
          },
          {
            title: "Campus Area",
            options: ["Northern Campus", "Southern Campus", "Other"]
          },
          {
            title: "Dorms Activities",
            options: ["Free sports / Fitness", "paid sports / Fitness", "Other Activities"]
          },
          {
            title: "24 Hours Reception",
            options: ["Dorms with 24/7 reception"]
          }
        ],
        checkboxs: []
      }
    }
  }
</script>

<style lang="scss">
@import '../../assets/styles/vars';
@import '../../assets/styles/mixins';

#filter{
  aside::-webkit-scrollbar {
      width: 0.5em;
  }
  
  aside::-webkit-scrollbar-track {
      -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.2);
  }
  
  aside::-webkit-scrollbar-thumb {
    background-color: $light-gray-color;
    outline: 1px solid slategrey;
    @include radius(10px);
  }
  #filters-heading{
    line-height: 50px;
    padding: 2px 15px 0;
    background: #ff884e;
    background: -webkit-linear-gradient(to right, #f9ba23, #ff884e); 
    background: linear-gradient(to right, #f9ba23, #ff884e); 
    font-size: 1.3em;
    color: #000;
    margin-bottom: 15px;
    width: 100%;
      .v-icon{
        color: #b75f11;
        margin-right: 6px;
        margin-left: 6px;
      }
  }
  #filters-body{
    padding: 10px 0px;
    .filter{
      margin-bottom: 10px;
      .filter-title{
        color: #585858;
        font-size: 1.2em;
        font-weight: 600;
        padding: 10px 10px 10px 30px;
      }
      ul{
        list-style: none;
        padding: 0;
          li{
            padding: 0px 0px 2px 30px;
            cursor: pointer;
            transition:all 0.2s;            
            .v-input,
            .v-input__slot{
              margin-top: 0px;
              margin-bottom: 0px;
            }
            .v-messages{
              display: none;
            }
            .v-label{
              line-height: 35px;
            }
            .v-input__control,
            .v-input__slot,
            .v-label{
              width: 100%;
              min-height: 30px;
            }
            &:hover{
              background: #ccfbde;
            }
            .v-input--selection-controls{
              padding: 0 !important;
            }
          }
      }
    }
  }
  .v-alert{
    margin: 0 10px;
    padding: 5px 15px 10px;
    font-size: 20px;
  }
  #rightside{
    padding: 30px 80px;

    @media (max-width: 600px) {
      padding: 30px 20px;
    }
  }
}
aside{
  margin-top:60px !important;
}
</style>