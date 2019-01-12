<template>
<v-layout justify-start row wrap id="dorm-card">
  <v-flex xs12>
    <v-card>
      <v-layout row wrap>

        <v-flex class="dorm-img" xs12 sm5 md4>

          <v-img :src="dorm.cover" gradient="to top right, rgba(44,40,72,.4), rgba(44,40,72,.4)" height="100%" width="100%">
            <v-layout slot="placeholder" fill-height align-center justify-center ma-0>
              <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
            </v-layout>
          </v-img>

        </v-flex>
        <v-flex class="dorm-details" xs12 sm7 md8>

          <v-card-title class="pa-0">
            <h3 class="headline">
              <router-link :to="'/dorms/'+ dorm.id">{{dorm.name}}</router-link>
            </h3>
          </v-card-title>

          <v-layout class="dorm-rating" row>
            <v-rating v-model="dorm.stars_average" length="5" readonly background-color="rgba(0,0,0,0.2)" color="yellow accent-4" empty-icon="$vuetify.icons.ratingFull" half-increments dense>
            </v-rating>
            <template v-if="dorm.number_of_reviews">
              <a href="#" @click.stop.prevent="showReviews(dorm.id)">{{dorm.number_of_reviews}} {{lang.dormCard.reviews}}</a>
            </template>
            <template v-else>
              <span>{{dorm.number_of_reviews}} {{lang.dormCard.reviews}}</span>
            </template>
          </v-layout>

          <v-layout class="dorm-address">
            <v-icon>place</v-icon>
            <span>{{dorm.address}}</span>
            <a href="#" @click.stop.prevent="showMap"> {{lang.dormCard.openMap}}</a>
          </v-layout>

          <template v-if=" dorm.rooms_left_in_dorm <= 10 ">
            <v-layout class="dorm-warning">
              <v-icon>warning</v-icon>
              <span>{{dorm.rooms_left_in_dorm}} {{lang.dormCard.roomsLeft}}</span>
            </v-layout>
          </template>
          

          <v-layout wrap class="dorm-features">

            <v-flex>
              <h3>{{lang.dormCard.dormFeatures}}:</h3>

              <v-tooltip top v-for="(feature, index) in dorm.features" :key="index">
                <v-icon class="facility-icon" slot="activator" v-if="feature.icon">{{feature.icon}}</v-icon>
                <v-icon class="facility-icon" slot="activator" v-else>fa-check</v-icon>
                <span>{{feature.name}}</span>
              </v-tooltip>

              <v-tooltip v-if="dorm.features.length > 10" top>
                <v-icon class="facility-icon" slot="activator" @click.stop.prevent="showFeatures">more_horiz</v-icon>
                <span>{{lang.dormCard.more}}</span>
              </v-tooltip>

            </v-flex>

          </v-layout>

        </v-flex>
        <div class="reviews-avarage" v-if="dorm.stars_average">
          {{dorm.stars_average}}
          <sub>/5</sub>
        </div>
        
      </v-layout>

      <v-divider light></v-divider>
      <v-layout>
        
        <v-card-actions justify-center align-center>
          <span class="price-bar__title">{{lang.dormCard.roomMatchesSearch}} :</span>
          <div class="rooms-price-bar">
            <div class="room-price" v-for="(room,index) in orderedRooms" :key="index">
              <v-tooltip top>
                <div @click="showRooms(room)" class="bar" slot="activator">
                  <v-icon>fa-bed</v-icon>
                </div>
                <span @click="showRooms(room)" class="price" slot="activator">{{$store.getters.activeCurrency}}{{room.price}}</span>
                <span>{{lang.dormCard.showDetails}}</span>
              </v-tooltip>

            </div>

          </div>

          <div>

            <v-bottom-sheet v-model="roomMode" lazy>
              <v-card>
                <v-layout class="room-card" row wrap>

                  <v-flex class="room-images" xs12 sm6>
                    <div class="close-room" @click="closeRoomModel">
                      <v-icon>fa-times</v-icon>
                    </div>
                    <v-carousel>
                      
                      <v-carousel-item v-for="(image,index) in room.photos" :key="index" :src="image.url">
                      </v-carousel-item>
                    </v-carousel>

                  </v-flex>

                  <v-flex class="room-details" xs12 sm6>
                    <v-layout row wrap justify-center>

                      <v-flex class="detail-block" xs6 md4>
                        <h3>{{lang.roomCard.roomType}}:</h3>
                        <span>{{room.room_type}}</span>
                      </v-flex>

                      <v-flex class="detail-block" xs6 md4>
                        <h3>{{lang.roomCard.peopleAllowed}}:</h3>
                        <span v-if="room.people_allowed_number < 4">
                          <v-icon v-for="n in room.people_allowed_number" :key="n">fa-user</v-icon>
                        </span>
                        <span v-else>
                          <v-icon>fa-user</v-icon>
                          X {{room.people_allowed_number}}
                        </span>
                      </v-flex>

                      <v-flex class="detail-block" xs12 md4>
                        <h3>{{lang.roomCard.price}}:</h3>
                        <span>{{$store.getters.activeCurrency}}{{room.price}}</span>
                      </v-flex>

                      <v-flex class="detail-block" xs12>
                        <template v-if=" room.rooms_left <= 5 ">
                          <div class="room-warning">
                            <v-icon small>fa-exclamation-triangle</v-icon>
                            <span>{{room.rooms_left}} {{lang.dormCard.roomsLeft}}</span>
                          </div>
                        </template>
                         <template v-else-if=" room.rooms_left <= 10 ">
                          <div class="room-info">
                            <v-icon>fa-exclamation-circle</v-icon>
                            <span>{{room.rooms_left}} {{lang.dormCard.roomsLeft}}</span>
                          </div>
                        </template>
                      </v-flex>

                      <v-flex class="feature-block" xs12 md6>
                        <h3>{{lang.roomCard.characteristics}}:</h3>
                        <div class="feature-block__scroll">
                          <div class="room-feature" v-for="(feature,index) in room.features" :key="index">
                            <v-icon v-if="feature.icon">{{feature.icon}}</v-icon>
                            <v-icon v-else>fa-check</v-icon>
                            <span>{{feature.name}}</span>
                          </div>
                        </div>
                      </v-flex>

                      <v-flex class="feature-block" xs12 md6>
                        <h3>{{lang.roomCard.features}}:</h3>
                        <div class="feature-block__scroll">
                          <div class="room-feature" v-for="(choice,index) in room.choices" :key="index">
                            <v-icon>fa-check</v-icon>
                            <span class="font-weight-bold">{{choice.filter_name}}: </span>
                            <span>{{choice.choice}}</span>
                          </div>
                        </div>
                      </v-flex>

                      <v-flex xs12>
                        <v-btn color="success" @click="reserveRoom(room)" class="reserve-btn elevation-0" large>{{lang.roomCard.reserveBtn}}</v-btn>
                        <v-btn  @click="saveRoom(room,dorm.id)" class="grey--text text--darken-2 elevation-0" large>{{lang.roomCard.aboutDormBtn}}</v-btn>

                      </v-flex>
                      <v-flex xs12>
                      </v-flex>
                    </v-layout>
                  </v-flex>

                </v-layout>
              </v-card>
            </v-bottom-sheet>

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
    <dorm-reviews :dormName="dorm.name" :reviews="dormReviews"></dorm-reviews>
  </v-dialog>

  <!-- Features Model -->
  <v-dialog v-model="featuresModel" lazy width="800px">
    <dorm-features :features="dorm.features" :dormName="dorm.name"></dorm-features>
  </v-dialog>

</v-layout>
</template>

<script src="./DormCard.js"></script>

<style src="./DormCard.scss" lang="scss"></style>
