<template>
<div id="manage-rooms">

  <v-layout wrap>

    <v-btn color="success" dark medium fixed bottom right fab @click="loadComponent('AddNewRoom')">
      <v-icon>add</v-icon>
    </v-btn>
    
    <v-flex xs12 md12 v-for="n in 5" :key="n">

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
          <!-- <v-flex xs12 md2>
            <h2>$1500</h2>
          </v-flex> -->

          <v-flex class="room-card__title" xs12 md8>
            <v-layout class="room-card__quantity" wrap>

              <v-flex xs12 sm6 md3>
                <h3>Total Rooms:</h3>
                <span>1250</span>
              </v-flex>

              <v-flex xs12 sm6 md3>
                <h3>Avaliable Rooms:</h3>
                <span>20</span>
              </v-flex>

              <v-flex xs12 sm6 md3>
                <h3>Reserved Rooms:</h3>
                <span>8</span>
              </v-flex>

              <v-flex xs12 sm6 md3>
                <h3>Quota:</h3>
                <v-layout wrap>
                  <v-flex sm8>
                    <v-text-field v-model="quota" type="number" min="0" required></v-text-field>
                  </v-flex>
                  <v-flex sm4>
                    <v-btn icon class="quota-update" dark>
                      <v-icon>fa-check</v-icon>
                    </v-btn>
                  </v-flex>

                </v-layout>
              </v-flex>

            </v-layout>
          </v-flex>

        </v-card-title>
      </v-card>

    </v-flex>

  </v-layout>
</div>
</template>

<script src="./ManageRooms.js"></script>

<style src="./ManageRooms.scss" lang="scss"></style>
