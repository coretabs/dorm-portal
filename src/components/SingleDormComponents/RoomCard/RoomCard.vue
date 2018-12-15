<template>
<v-flex md8 xs12 id="room-card">
  <v-card>
    <v-layout row wrap>
      <v-flex class="room-images" xs12 sm8>
        <v-carousel>
          <!-- TODO: Update images to be fetched from the endpoint -->
          <v-carousel-item v-for="(image,index) in photos" :key="index" :src="image"></v-carousel-item>
        </v-carousel>
      </v-flex>
      <v-flex class="room-details" xs12 sm4>
        <v-layout row wrap justify-center align-center>
          <v-flex class="detail-block" xs6>
            <h3>Room Type:</h3>
            <span>{{room.room_type}}</span>
          </v-flex>
          
          <v-flex class="detail-block" xs6>
            <h3>Number of People:</h3>
            <span v-if="room.people_allowed_number < 4">
              <v-icon v-for="n in room.people_allowed_number" :key="n">fa-user</v-icon>
            </span>
            <span v-else>
              <v-icon>fa-user</v-icon>
              X {{room.people_allowed_number}}
            </span>
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

          <v-flex class="feature-block" xs12>
            <h3>Room Features:</h3>
            <!-- TODO: Update features to be fetched from the endpoint -->
            <div class="feature-block__scroll">
              <div class="room-feature" v-for="(feature,index) in room.features" :key="index">
                <v-icon>{{feature.icon}}</v-icon>
                <span>{{feature.name}}</span>
              </div>
              <div class="room-feature" v-for="(choices,index) in room.choices" :key="index">
                <v-icon>fa-check</v-icon>
                <span class="font-weight-medium">{{choices.filter_name}}:</span> <span> {{choices.choice}}</span>
              </div>
            </div>
          </v-flex>


          
        </v-layout>
        <v-layout class="reservation-block" row wrap justify-center align-center>
          <v-flex class="room-price" xs6>
            <h3>Price:</h3>
            <span>{{$store.getters.activeCurrency}}{{room.price}}</span>
          </v-flex>
          <v-flex class="reserve-btn" xs6>
            <v-btn color="success" @click="reserveRoom(room)" class="elevation-0">Reserve Now</v-btn>
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-card>
</v-flex>
</template>

<script src="./RoomCard.js"></script>

<style src="./RoomCard.scss" lang="scss"></style>
