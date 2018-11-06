<template>
      <v-layout justify-start row wrap id="card">
        <v-flex xs12 sm10>
          <v-card>
            <v-layout row wrap>
              <v-flex class="dorm-img" xs12 sm4>
                <img src="https://cdn.vuetifyjs.com/images/cards/desert.jpg" alt="">
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
                  <a href="#">{{reviewsNumber}} reviews</a>
                </v-layout>

                <v-layout class="dorm-address">
                  <v-icon>place</v-icon>
                  <span>Address of the dorm </span>
                  <a href="#"> open map</a>
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
                      >local_parking</v-icon>
                      <span>Free Parking</span>
                    </v-tooltip>

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >wifi</v-icon>
                      <span>Free wifi</span>
                    </v-tooltip>

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >wifi</v-icon>
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

                  <v-flex>
                  <h3>Popular Activities:</h3>

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >local_parking</v-icon>
                      <span>Free Parking</span>
                    </v-tooltip>

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >wifi</v-icon>
                      <span>Free wifi</span>
                    </v-tooltip>
                    

                    <v-tooltip top>
                      <v-icon class="facility-icon" slot="activator"
                      >wifi</v-icon>
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
      </v-layout>
</template>

<script>
  export default {
    name: 'DormCard',
    data: function (){
      return{
        rating: 4,
        reviewsNumber: 126,
        roomsLeft: 7
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
      img{
        height: 100%;
      }
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
      margin: 20px 0;
      font-size: 16px;
      .v-icon{
        color: #e33333;
        font-size: 20px;
        margin-right: 10px;
      }
    }
    .dorm-facilities{
      h3{
        margin: 15px 0;
        color: $gray-color
      }
      .facility-icon{
        width: 40px;
        height: 40px;
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
      height: 6px;
      width: 95%;
      margin: 0 auto;
      position: relative;
      background-color: $light-gray-color;
    }
  }
}
</style>