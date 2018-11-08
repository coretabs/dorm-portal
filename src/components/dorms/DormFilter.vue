<template>

  <div id="filter">

    <!-- filters sidebar -->
    <v-navigation-drawer
      :clipped="$vuetify.breakpoint.lgAndUp"
      v-model="drawer"
      width="320"
      fixed app>
      <template>
        <div id="filters-heading"><v-icon left>filter_list</v-icon> {{filtersHeading}}</div>
        <div id="filters-body">

          <div class="filter" v-for= "(filter,index) in filters" :key="index">
            <div class="filter-title">{{filter.name}}</div>
            <template v-if="filter.checkbox">
              <ul>
                  <li v-for= "(option, index) in filter.options" :key="index">
                    <v-checkbox :value="option.option_id" :label="option.name" color="success"></v-checkbox>
                  </li>
              </ul>
            </template>
            <template v-if="filter.integral">
                <div>
                               
                  <v-layout class="integral-filter" row>
                    <v-flex class="px-3">
                      <v-range-slider 
                        thumb-label="always"
                        thumb-color="#3ab86c"
                        v-model="filter.value"
                        :max="filter.max_value"
                        :min="filter.min_value"
                        :step="1"
                        color="success"
                      ></v-range-slider>
                    </v-flex>
                   </v-layout>
                   <v-layout class="integral-filter" v-show="false" row>
                     <v-flex  class="integral-input">
                        <v-text-field
                          label="From"
                          v-model="filter.value[0]"
                          class="mt-0"
                          hide-details
                          type="text"
                          disabled
                        ></v-text-field>
                      </v-flex>
                      <v-flex  class="integral-input">
                        <v-text-field
                          label="To"
                          v-model="filter.value[1]"
                          class="mt-0"
                          hide-details
                          type="text"
                          disabled
                        ></v-text-field>
                      </v-flex>
                    </v-layout>   
              </div>
              
            </template>
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
            </v-flex> -->

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
                "id": "1",
                "name": "24 Hours Reception",
                "checkbox": true,
                "integral": false,
                "options": [
                    {
                        "option_id": 1,
                        "name": "Dorms with 7/24 open reception"
                    }
                ]
            },
            {
                "id": "3",
                "name": "Dorms Activities",
                "checkbox": true,
                "integral": false,
                "options": [
                    {
                        "option_id": 1,
                        "name": "Free sport/Fitness"
                    },
                    {
                        "option_id": 2,
                        "name": "Paid sport/Fitness"
                    },
                    {
                        "option_id": 3,
                        "name": "Other activities"
                    }
                ]
            },
            {
                "id": "3",
                "name": "Meals",
                "checkbox": true,
                "integral": false,
                "options": [
                    {
                        "option_id": 1,
                        "name": "3 meals included"
                    },
                    {
                        "option_id": 2,
                        "name": "Breakfast included"
                    },
                    {
                        "option_id": 3,
                        "name": "Breakfast/Dinner included"
                    }
                ]
            },
            {
                "id": "4",
                "name": "Shopping Opportunity",
                "checkbox": true,
                "integral": false,
                "options": [
                    {
                        "option_id": 1,
                        "name": "Restorant/Cafeteria"
                    },
                    {
                        "option_id": 2,
                        "name": "Hairdresser/Barber"
                    },
                    {
                        "option_id": 3,
                        "name": "Market"
                    }
                ]
            },
            {
                "id": "5",
                "name": "Price Range",
                "integral": true,
                "checkbox": false,
                "min_value": "0",
                "max_value":"2000",
                 value: [0, 2000]
            }
          ]
      }
    }, 
    methods:{
      test(){
        alert(this.filter_gourps[1].value)
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
    width: 100%;
      .v-icon{
        color: #b75f11;
        margin-right: 6px;
        margin-left: 6px;
      }
  }
  #filters-body{
     background: #fcfcfc;
     padding: 20px 0px;
    .filter{
      margin-bottom: 15px;
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
  .integral-filter{
    max-width: 80%;
    margin: 20px auto 0;
    .integral-input{
      width: 150px;
    }
    .v-text-field{
      margin:0 15px; 
    }
    &:nth-child(2){
      margin: 0px auto 0;
    }
    .v-messages{
      display: none;
    }
  }
}
aside{
  margin-top:60px !important;
}
</style>