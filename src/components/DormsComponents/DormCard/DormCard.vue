<template>
<v-layout justify-start row wrap id="dorm-card">
  <v-flex xs12>
    <v-card>
      <v-layout row wrap>

        <v-flex class="dorm-img" xs12 sm4>

          <v-img :src="dorm.cover" gradient="to top right, rgba(44,40,72,.4), rgba(44,40,72,.4)" height="100%" width="100%"></v-img>

        </v-flex>

        <v-flex class="dorm-details" xs12 sm8>

          <v-card-title class="pa-0">
            <h3 class="headline">
              <router-link to="/dorms/5">{{dorm.name}}</router-link>
            </h3>
          </v-card-title>

          <v-layout class="dorm-rating" row>
            <v-rating v-model="dorm.stars" length="5" readonly background-color="rgba(0,0,0,0.2)" color="yellow accent-4" empty-icon="$vuetify.icons.ratingFull" half-increments dense>
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

          <v-layout wrap class="dorm-features">

            <v-flex>
              <h3>{{lang.dormCard.dormFeatures}}:</h3>

              <v-tooltip top v-for="(feature, index) in popularFeatures" :key="index">
                <v-icon class="facility-icon" slot="activator">{{feature.icon}}</v-icon>
                <span>{{feature.name}}</span>
              </v-tooltip>

              <v-tooltip top>
                <v-icon class="facility-icon" slot="activator" @click.stop.prevent="showFeatures">more_horiz</v-icon>
                <span>{{lang.dormCard.more}}</span>
              </v-tooltip>

            </v-flex>

          </v-layout>

        </v-flex>
        <div class="reviews-avarage">{{dorm.stars}}</div>
      </v-layout>

      <v-divider light></v-divider>

      <v-layout>
        <v-card-actions justify-center align-center>
          <div class="rooms-price-bar">

            <div class="room-price" v-for="(room,index) in dorm.rooms" :key="index">
              <v-tooltip top>
                <div @click="showRooms(room)" class="bar" slot="activator"></div>
                <span @click="showRooms(room)" class="price" slot="activator">${{room.price}}</span>
                <span>Click To show room details</span>
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
                      <v-carousel-item v-for="(image,index) in room.photos" :key="index" :src="image"></v-carousel-item>
                    </v-carousel>

                  </v-flex>

                  <v-flex class="room-details" xs12 sm6>
                    <v-layout row wrap justify-center align-center>

                      <v-flex class="detail-block" xs6 md4>
                        <h3>Room Type:</h3>
                        <span>{{room.room_type}}</span>
                      </v-flex>

                      <v-flex class="detail-block" xs6 md4>
                        <h3>Number of People:</h3>
                        <span>
                              <v-icon>fa-user</v-icon>
                              X {{room.people_number}}
                            </span>
                      </v-flex>

                      <v-flex class="detail-block" xs12 md4>
                        <h3>Price:</h3>
                        <span>${{room.price}}</span>
                      </v-flex>

                      <v-flex class="detail-block" xs12>
                        <div class="room-warning">
                          <v-icon>warning</v-icon>
                          <span>5 {{lang.dormCard.roomsLeft}}</span>
                        </div>
                      </v-flex>

                      <v-flex class="feature-block" xs12>
                        <h3>Room Features:</h3>
                        <div class="room-feature" v-for="(feature,index) in room.features" :key="index">
                          <v-icon>{{feature.icon}}</v-icon>
                          <span>{{feature.name}}</span>
                        </div>
                      </v-flex>
                      
                      <v-flex xs12>
                        <v-btn color="success" to="/reservation" class="reserve-btn elevation-0" large>Reserve Now</v-btn>
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
    <dorm-reviews :dormName="dorm.name"></dorm-reviews>
  </v-dialog>

  <!-- Features Model -->
  <v-dialog v-model="featuresModel" lazy width="800px">
    <dorm-features :features="dorm.features" :dormName="dorm.name"></dorm-features>
  </v-dialog>

</v-layout>
</template>

<script src="./DormCard.js"></script>

<style src="./DormCard.scss" lang="scss"></style>
