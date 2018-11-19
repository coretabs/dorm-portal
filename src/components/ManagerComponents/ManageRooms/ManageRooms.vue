<template>
<div id="manage-rooms">
  <v-layout wrap>
    <v-btn color="success" dark medium fixed bottom right fab @click="loadComponent('AddNewRoom')">
      <v-icon>add</v-icon>
    </v-btn>
    <v-flex xs12 v-for="n in 5" :key="n">
      <v-card id="room-card">
        <v-menu bottom left class="room-card__actions absolute-menu">
          <v-btn slot="activator" icon>
            <v-icon>more_vert</v-icon>
          </v-btn>
          <v-list>
            <v-list-tile v-for="(item, i) in items" :key="i">
              <v-list-tile-title>{{ item.title }}</v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-menu>
        <v-card-title primary-title>
          <v-flex class="room-card__title" xs12 md3 px-3>
            <v-layout wrap>
              <v-flex class="room-card__title" xs12>
                <h3>Room Type:</h3>
                <span>Single room</span>
                <v-btn slot="activator" icon>
                  <v-icon>fa-info</v-icon>
                </v-btn>
              </v-flex>
            </v-layout>
          </v-flex>
          <v-flex class="room-card__title" xs12 md8>
            <v-layout class="room-card__quantity" wrap>
              <v-flex xs12 sm6 md8>
                <h3>Reserved Rooms:</h3>
                <v-layout row wrap>
                  <v-flex xs12 md2>
                    <span>20<sub>/100</sub></span>
                  </v-flex>
                  <v-flex xs12 md10>
                    <v-progress-linear class="room-card__progress" color="green" height="25" value="20"></v-progress-linear>
                  </v-flex>
                </v-layout>
                <!-- <span>0<sub>/50</sub></span> -->
              </v-flex>

              <v-flex xs12 sm6 md4>
                <h3>Quota:</h3>
                <v-layout row>
                  <span>0</span>
                  <v-btn icon class="quota-update" dark @click="showQuotaUpdate = true">
                    <v-icon small>fa-pencil-alt</v-icon>
                  </v-btn>
                </v-layout>
              </v-flex>
            </v-layout>
          </v-flex>
        </v-card-title>
      </v-card>
    </v-flex>
  </v-layout>
  <v-layout row justify-center>
    <v-dialog v-model="showQuotaUpdate" persistent max-width="350">
      <v-card>
        <v-card-text>
          <h2>Update Quota:</h2>
          <p class="avaliable-quota__info">You can add upto <strong>45</strong> room</p>
          <p class="avaliable-quota__warning">You have <strong>0</strong> room to add</p>
          <v-text-field v-model="quota" type="number" min="0" required></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" flat @click="showQuotaUpdate = false">Cancel</v-btn>
          <v-btn color="green darken-1" flat @click="showQuotaUpdate = false">Confirm</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</div>
</template>

<script src="./ManageRooms.js"></script>

<style src="./ManageRooms.scss" lang="scss"></style>
