<template>

  <div id="filters">
        <v-navigation-drawer
      :clipped="$vuetify.breakpoint.lgAndUp"
      v-model="drawer"
      app
      >

        <template>
          <div id="filters-heading"><v-icon left>filter_list</v-icon> {{filtersHeading}}</div>

          <div id="filters-body">
            <div class="filter" v-for= "(filter,index) in filters" :key="index">
              <div class="filter-title">{{filter.title}}</div>
              <ul>
                <li v-for= "(option, index) in filter.options" :key="index">
                <v-checkbox v-model="checkboxs" :value="option" :label="option"></v-checkbox>
                </li>
              </ul>
            </div>
          </div>


          <!-- <v-list-tile v-for= "(filter,index) in filters" :key="index" @click="">
            <v-list-tile-action>
              <v-checkbox v-model="checkboxs" :value="option"></v-checkbox>
            </v-list-tile-action>
            <v-list-tile-content @click="checkboxs = !checkboxs">
              <v-list-tile-title>{{filter.title}}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile> -->

        </template>

    </v-navigation-drawer>
  </div>

</template>

<script>
  export default {
    name: 'DormFilter',
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
    },
    props: {
      source: String
    }
  }
</script>

<style lang="scss" scoped>
@import '../../assets/styles/vars';
@import '../../assets/styles/mixins';
#filters{
  *{
    box-sizing: border-box;
    outline: none;
  }
  width: $filtersAside-width;
  height: auto;
  padding-bottom: 10px;
  background-color: #fcfcfc;
  border-right: 1px solid rgba(0,0,0,0.1);
  position: relative;
  overflow: hidden;
  #filters-heading{
    line-height: 45px;
    padding: 2px 15px 0;
    background: #ff884e;
    background: -webkit-linear-gradient(to right, #f9ba23, #ff884e); 
    background: linear-gradient(to right, #f9ba23, #ff884e); 
    border-right: 1px solid rgba(0,0,0,.1);
    font-size: 1.3em;
    color: #000;
    z-index: 1;
    position: fixed;
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
            padding: 0px 0px 5px 30px;
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
            .v-input--is-label-active .theme--light.v-icon{
              color: #68cf91 !important;
            }
            .theme--light.v-icon{
              color: #aaa !important;
            }
            .v-label{
              padding: 6px 20px 4px 0;
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
          }
      }
    }
  }
}
aside{
  margin-top:60px !important;
}
</style>