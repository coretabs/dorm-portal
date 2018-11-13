<template>
<v-flex md8 xs12 id="room-card">
  <v-card>
    <v-layout row wrap>

      <v-flex class="room-img" xs12 sm8>

        <swiper :options="swiperOption">
          <swiper-slide>
            <v-img position src="https://images.pexels.com/photos/279719/pexels-photo-279719.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260" gradient="to top right, rgba(44,40,72,.4), rgba(44,40,72,.4)"></v-img>
          </swiper-slide>
          <swiper-slide>
            <v-img position src="https://images.pexels.com/photos/1326946/pexels-photo-1326946.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260" gradient="to top right, rgba(44,40,72,.4), rgba(44,40,72,.4)"></v-img>
          </swiper-slide>
          <swiper-slide>
            <v-img position src="https://images.pexels.com/photos/279719/pexels-photo-279719.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260" gradient="to top right, rgba(44,40,72,.4), rgba(44,40,72,.4)"></v-img>
          </swiper-slide>
          <div class="swiper-pagination" slot="pagination"></div>
          <div class="swiper-button-prev" slot="button-prev"></div>
          <div class="swiper-button-next" slot="button-next"></div>
        </swiper>

      </v-flex>

      <v-flex class="room-details" xs12 sm4>

        <v-layout row wrap justify-center align-center>

          <v-flex class="detail-block" xs6 sm6>
            <h3>Room Type:</h3>
            <span>Suit Room</span>
          </v-flex>

          <v-flex class="detail-block" xs6 sm6>
            <h3>Number of People:</h3>
            <span>
                <v-icon>fa-user</v-icon>
                X 2
              </span>
          </v-flex>

         

          <v-flex class="detail-block" xs12>
            <div class="room-warning">
              <v-icon>warning</v-icon>
              <span>5 {{lang.dormCard.roomsLeft}}</span>
            </div>
          </v-flex>

          <v-flex class="feature-block" xs12>
            <h3>Room Features:</h3>
            <div class="room-feature" v-for="(feature,index) in features" :key="index">
              <v-icon>{{feature.icon}}</v-icon>
              <span>{{feature.name}}</span>
            </div>
          </v-flex>

          <v-flex class="room-price" xs6 sm6>
            <h3>Price:</h3>
            <span>$1555</span>
          </v-flex>

          <v-flex class="reserve-btn" sm6>
            <v-btn color="success" class="elevation-0">Reserve Now</v-btn>
          </v-flex> 

        </v-layout>

        <!-- <v-layout row wrap class="room-facilities">
          <v-flex xs12>
              <h3>Room Features:</h3>
              <v-tooltip top v-for="n in 14" :key="n">
                <v-icon class="facility-icon" slot="activator">fa-wifi</v-icon>
                <span>free wifi</span>
              </v-tooltip>
              <v-tooltip top>
                <v-icon class="facility-icon" slot="activator">more_horiz</v-icon>
                <span>{{lang.dormCard.more}}</span>
              </v-tooltip>
            </v-flex>
        </v-layout> -->

      </v-flex>
    </v-layout>

  </v-card>
  
</v-flex>
</template>

<script src="./RoomCard.js"></script>

<style src="./RoomCard.scss" lang="scss"></style>
