<template>
<div>
  <div v-if="showSavedRoomNav" id="show-savedroom">
    <span>The room you have choosen is saved</span>
    <v-btn depressed color="#ea7e15" class="font-weight-bold" @click="showRoomModel">Check it again</v-btn>
    <v-btn color="#c61a1a" class="font-weight-bold" @click="deleteSavedRoom">
      <v-icon small left>fa-trash-alt</v-icon> Delete it
    </v-btn>
  </div>

  <v-bottom-sheet v-model="showSavedRoomModel" lazy>
    <v-card>
      <v-layout class="room-card" row wrap>

        <v-flex class="room-images" xs12 sm6>
          <div class="close-room" @click="closeRoomModel">
            <v-icon>fa-times</v-icon>
          </div>
          <v-carousel>
            <v-carousel-item v-for="(image,index) in savedRoom.room.photos" :key="index" :src="image"></v-carousel-item>
          </v-carousel>

        </v-flex>

        <v-flex class="room-details" xs12 sm6>
          <v-layout row wrap justify-center align-center>

            <v-flex class="detail-block" xs6 md4>
              <h3>Room Type:</h3>
              <span>{{savedRoom.room.room_type}}</span>
            </v-flex>

            <v-flex class="detail-block" xs6 md4>
              <h3>Number of People:</h3>
              <span v-if="savedRoom.room.people_allowed_number < 4">
                          <v-icon v-for="n in savedRoom.room.people_allowed_number" :key="n">fa-user</v-icon>
                        </span>
              <span v-else>
                          <v-icon>fa-user</v-icon>
                          X {{savedRoom.room.people_allowed_number}}
                        </span>
            </v-flex>

            <v-flex class="detail-block" xs12 md4>
              <h3>Price:</h3>
              <span>${{savedRoom.room.price}}</span>
            </v-flex>

            <v-flex class="detail-block" xs12>
              <template v-if=" savedRoom.room.rooms_left <= 5 ">
                <div class="room-warning">
                  <v-icon small>fa-exclamation-triangle</v-icon>
                  <span>{{savedRoom.room.rooms_left}} {{lang.dormCard.roomsLeft}}</span>
                </div>
              </template>
              <template v-else-if=" savedRoom.room.rooms_left <= 10 ">
                <div class="room-info">
                  <v-icon>fa-exclamation-circle</v-icon>
                  <span>{{savedRoom.room.rooms_left}} {{lang.dormCard.roomsLeft}}</span>
                </div>
              </template>
            </v-flex>

            <v-flex class="feature-block" xs12 md6>
              <h3>Room characteristics:</h3>
              <div class="feature-block__scroll">
                <div class="room-feature" v-for="(feature,index) in savedRoom.room.features" :key="index">
                  <v-icon>{{feature.icon}}</v-icon>
                  <span>{{feature.name}}</span>
                </div>
              </div>
            </v-flex>

            <v-flex class="feature-block" xs12 md6>
              <h3>Room Features:</h3>
              <div class="feature-block__scroll">
                <div class="room-feature" v-for="(choice,index) in savedRoom.room.choices" :key="index">
                  <v-icon>fa-check</v-icon>
                  <span class="font-weight-bold">{{choice.filter_name}}: </span>
                  <span>{{choice.choice}}</span>
                </div>
              </div>
            </v-flex>

            <v-flex xs12>
              <v-btn color="success" @click="reserveRoom(savedRoom.room)" class="reserve-btn elevation-0" large>Reserve Now</v-btn>
            </v-flex>
          </v-layout>
        </v-flex>

      </v-layout>
    </v-card>
  </v-bottom-sheet>

</div>
</template>

<script src="./SingleRoomCard.js"></script>

<style src="./SingleRoomCard.scss" lang="scss"></style>
