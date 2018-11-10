<template>
      <v-layout justify-start row wrap id="card">
        <v-flex md10 xs12>
          <v-card>
            <v-layout row wrap>

              <v-flex class="dorm-img" xs12 sm4>
                <v-img :src="dorm.cover" 
                gradient="to top right, rgba(44,40,72,.4), rgba(44,40,72,.4)"
                height="100%" width="100%"></v-img>
              </v-flex>
              
              <v-flex class="dorm-details" xs12 sm8>

                <v-card-title class="pa-0">
                    <h3 class="headline">
                      <a href="#">{{dorm.name}}</a>
                    </h3>
                </v-card-title>

                <v-layout class="dorm-rating" row>
                  <v-rating
                    v-model="dorm.stars"
                    length="5"
                    readonly
                    background-color="rgba(0,0,0,0.2)"
                    color="yellow accent-4"
                    empty-icon="$vuetify.icons.ratingFull"
                    half-increments
                    dense>
                  </v-rating>
                  <a href="#" @click.stop.prevent="showReviews">{{dorm.number_of_reviews}} {{lang.dormCard.reviews}}</a>
                </v-layout>

                <v-layout class="dorm-address">
                  <v-icon>place</v-icon>
                  <span>{{dorm.address}}</span>
                  <a href="#" @click.stop.prevent="showMap"> {{lang.dormCard.openMap}}</a>
                </v-layout>
                
                <template v-if=" roomsLeft <= 10 ">
                  <v-layout class="dorm-warning">
                    <v-icon>warning</v-icon>
                    <span>{{roomsLeft}} {{lang.dormCard.roomsLeft}}</span>
                  </v-layout>
                </template>

                <v-layout wrap class="dorm-facilities">

                  <v-flex>
                    <h3>{{lang.dormCard.popularFacilities}}:</h3>

                    <v-tooltip top v-for="(facility, index) in popularFacilities" :key="index">
                      <v-icon class="facility-icon" slot="activator"
                      >{{facility.icon}}</v-icon>
                      <span>{{facility.name}}</span>
                    </v-tooltip>

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >more_horiz</v-icon>
                      <span>{{lang.dormCard.more}}</span>
                    </v-tooltip>
                    
                  </v-flex>

                  <v-flex>
                    <h3>{{lang.dormCard.popularActivities}}:</h3>

                    <v-tooltip top v-for="(activity, index) in popularActivities" :key="index">
                      <v-icon class="facility-icon" slot="activator"
                      >{{activity.icon}}</v-icon>
                      <span>{{activity.name}}</span>
                    </v-tooltip>

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >more_horiz</v-icon>
                      <span>{{lang.dormCard.more}}</span>
                    </v-tooltip>

                  </v-flex>

                </v-layout>
                
              </v-flex>
              
            </v-layout>

            <v-divider light></v-divider>

            <v-layout>
              <v-card-actions justify-center align-center>
                <div class="price-bar">
                  
                </div>
              </v-card-actions>
            </v-layout>

          </v-card>

        </v-flex>
        <!-- Map Model -->
        <v-dialog v-model="mapModel" lazy width="800px">
            <dorm-map :longitude="dorm.geo_longitude" :latitude="dorm.geo_latitude"></dorm-map>
        </v-dialog>

        <!-- Reviews Model -->
        <v-dialog v-model="reviewsModel" lazy width="800px">
            <dorm-reviews></dorm-reviews>
        </v-dialog>

      </v-layout>
</template>

<script>
  import DormMap from './DormMap'
  import DormReviews from './DormReviews'

  export default {
    name: 'DormCard',
    components: {
      'dorm-map': DormMap,
      'dorm-reviews' : DormReviews
    },
    props:{
      'dorm': {}
    },
    data: function (){
      return{
        mapModel: false,
        reviewsModel: false,
        roomsLeft : this.dorm.number_of_found_rooms
      }
    },
    methods: {
      showMap(){
        this.mapModel = !this.mapModel
      },
      showReviews(){
        this.reviewsModel = !this.reviewsModel
      }
    },
    computed:{
      popularFacilities(){
        return this.dorm.facilities.slice(0, 4)
      },
      popularActivities(){
        return this.dorm.activities.slice(0, 4)
      },
      lang(){ return this.$store.state.language }
    }
  }
</script>

<style lang="scss">
@import '../../assets/styles/vars';
@import '../../assets/styles/mixins';

#card{
  margin: 0 0 40px;
  
  .v-card{
    box-shadow: none;
    border:1px solid $light-gray-color;
    @include radius(5px);   
    overflow: hidden;
    .headline{
      margin: 10px 5px;
      a{
        font-weight: 500;
        font-size: 28px !important;
        text-decoration: none;
        color: $light-black;
      }
    }
    .dorm-img{
      overflow: hidden;
      min-height: 250px;
      // img{
      //   height: 100%;
      // }
    }
    .dorm-details{
      padding: 20px 30px;
      .dorm-rating a{
        color: $gray-color;
        display: inline-block;
        margin: 2px 0 0 6px;
        font-size: 16px;
      }
    }
    .dorm-address{
      margin-top: 25px;
      .v-icon{
        font-size: 20px;
        color: $gray-color;
        margin-right: 5px;
      }
      span::after{
        content: "-";
        display: inline-block;
        padding:0 3px;
      }
    }
    .dorm-warning{
      background-color: #fafafa;
      padding: 10px 15px;
      border-left: 5px solid #e33333;
      margin: 20px 0 10px 6px;
      font-size: 16px;
      .v-icon{
        color: #e33333;
        font-size: 20px;
        margin-right: 10px;
      }
    }
    .dorm-facilities{
      margin: 15px 0 0 6px;

      h3{
        margin: 15px 0 15px;
        color: $gray-color
      }
      .facility-icon{
        width: 40px;
        height: 40px;
        font-size: 20px;
        @include radius(50%);
        border: 2px solid #ccc;
        text-align: center;
        line-height: 40px;
        cursor: pointer;
        margin: 0 10px 10px 0;
      }
    }
  }
  .v-card__actions{
    background: #fbfbfb;
    width: 100%;
    min-height: 180px;
    .price-bar{
      height: 5px;
      width: 95%;
      margin: 0 auto;
      position: relative;
      background-color: $light-gray-color;
    }
  }
}
</style>