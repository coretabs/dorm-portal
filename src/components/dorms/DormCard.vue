<template>
      <v-layout justify-start row wrap id="card">
        <v-flex md10 xs12>
          <v-card>
            <v-layout row wrap>
              
              <v-flex class="dorm-img" xs12 sm4>
                <!-- <img src="https://cdn.vuetifyjs.com/images/cards/desert.jpg" alt=""> -->
                <v-img src="https://en.alfamcyprus.com/thumbnail.php?file=pics/pics_slider/89d3badf6d8421039a1ccf3b5ad2a191.jpg&pwidth=1903&pheight=850&pw=475.7500&ph=212.5000&px=0.0000&py=67.0000&pscale=0.2478&pangle=0.0000&force=y" 
                gradient="to top right, rgba(44,40,72,.4), rgba(44,40,72,.4)"
                height="100%" width="100%"></v-img>
              </v-flex>
              
              <v-flex class="dorm-details" xs12 sm8>

                <v-card-title class="pa-0">
                    <h3 class="headline">
                      <a href="#">Alfam Dorm</a>
                    </h3>
                </v-card-title>

                <v-layout class="dorm-rating" row>
                  <v-rating
                    v-model="rating"
                    length="5"
                    readonly
                    background-color="rgba(0,0,0,0.2)"
                    color="yellow accent-4"
                    empty-icon="$vuetify.icons.ratingFull"
                    half-increments
                    dense>
                  </v-rating>
                  <a href="#" @click.stop.prevent="showReviews">{{reviewsNumber}} reviews</a>
                </v-layout>

                <v-layout class="dorm-address">
                  <v-icon>place</v-icon>
                  <span>Address of the dorm </span>
                  <a href="#" @click.stop.prevent="showMap"> open map</a>
                </v-layout>
                
                <v-layout class="dorm-warning">
                  <v-icon>warning</v-icon>
                  <span>Only {{roomsLeft}} rooms left</span>
                </v-layout>

                <v-layout wrap class="dorm-facilities">

                  <v-flex>
                  <h3>Popular Facilities:</h3>

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >fa-parking</v-icon>
                      <span>Free Parking</span>
                    </v-tooltip>

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >fa-wifi</v-icon>
                      <span>Free wifi</span>
                    </v-tooltip>

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >fa-utensils</v-icon>
                      <span>Restaurant</span>
                    </v-tooltip>

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >fa-bus</v-icon>
                      <span>Free Transportation</span>
                    </v-tooltip>

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >more_horiz</v-icon>
                      <span>more</span>
                    </v-tooltip>
                    
                  </v-flex>

                  <v-flex>
                  <h3>Popular Activities:</h3>

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >fa-swimmer</v-icon>
                      <span>Free Parking</span>
                    </v-tooltip>

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >fa-futbol</v-icon>
                      <span>Free wifi</span>
                    </v-tooltip>
                    

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >fa-handshake</v-icon>
                      <span>Free wifi</span>
                    </v-tooltip>

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >wifi</v-icon>
                      <span>Free wifi</span>
                    </v-tooltip>

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >more_horiz</v-icon>
                      <span>more</span>
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
            <dorm-map></dorm-map>
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
    data: function (){
      return{
        mapModel: false,
        reviewsModel: false,
        rating: 4,
        reviewsNumber: 126,
        
      }
    },
    methods: {
      showMap(){
        this.mapModel = !this.mapModel
      },
      showReviews(){
        this.reviewsModel = !this.reviewsModel
      }
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
        padding-right: 3px;
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