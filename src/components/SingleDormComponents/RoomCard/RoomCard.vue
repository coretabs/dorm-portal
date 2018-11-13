<template>
<v-flex md8 xs12 id="room-card">
  <v-card>
    <v-layout row wrap>

      <v-flex class="room-img" xs12 sm4>
        <v-img src="https://images.pexels.com/photos/279719/pexels-photo-279719.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260" gradient="to top right, rgba(44,40,72,.4), rgba(44,40,72,.4)" height="100%" width="100%"></v-img>
      </v-flex>

      <v-flex class="room-details" xs12 sm8>

        <v-layout row wrap>

          <v-flex sm3>
              <h3>Room Type:</h3>
              <span>Suit Room</span>
          </v-flex>

          <v-flex sm3>
              <h3>Number of People:</h3>
              <span>
                <v-icon>fa-user</v-icon>
                X 2
              </span>
          </v-flex>

          <v-flex sm3>
              <h3>Price:</h3>
              <span>$1555</span>
          </v-flex>

          <v-flex sm3>
              <v-btn color="success" class="elevation-0">Reserve Now</v-btn>
          </v-flex>

        </v-layout>

        <template>
            <v-layout class="room-warning">
              <v-icon>warning</v-icon>
              <span>5 {{lang.dormCard.roomsLeft}}</span>
            </v-layout>
          </template>
        <v-layout row wrap class="room-facilities">

          <v-flex xs12 >
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

        </v-layout>

        
        
      </v-flex>

    </v-layout>

  </v-card>

</v-flex>
</template>

<script src="./RoomCard.js"></script>

<style src="./RoomCard.scss" lang="scss"></style>
