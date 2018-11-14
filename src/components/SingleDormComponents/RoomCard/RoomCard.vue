<template>
<v-flex md8 xs12 id="room-card">
  <v-card>
    <v-layout row wrap>

      <v-flex class="room-images" xs12 sm8>

        <v-carousel>
          <v-carousel-item v-for="(image,index) in photos" :key="index" :src="image"></v-carousel-item>
        </v-carousel>

      </v-flex>

      <v-flex class="room-details" xs12 sm4>

        <v-layout row wrap justify-center align-center>

          <v-flex class="detail-block" xs6>
            <h3>Room Type:</h3>
            <span>Suit Room</span>
          </v-flex>

          <v-flex class="detail-block" xs6>
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
        </v-layout>

        <v-layout class="reservation-block" row wrap justify-center align-center>

          <v-flex class="room-price" xs6>
            <h3>Price:</h3>
            <span>$1555</span>
          </v-flex>

          <v-flex class="reserve-btn" xs6>
            <v-btn color="success" class="elevation-0">Reserve Now</v-btn>
          </v-flex>

        </v-layout>
      </v-flex>
    </v-layout>

  </v-card>

</v-flex>
</template>

<script src="./RoomCard.js"></script>

<style src="./RoomCard.scss" lang="scss"></style>
