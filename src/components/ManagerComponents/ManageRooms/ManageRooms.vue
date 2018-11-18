<template>
<div id="manage-rooms">

  <!-- <v-layout row wrap>
     <v-expansion-panel
      v-model="panel"
      expand
    >
      <v-expansion-panel-content
        v-for="(item, i) in 5"
        :key="i"
      >
        <div slot="header">
          <v-layout row>
          <v-flex xs12>
            <h3>Single room</h3>
            <span>Full Acadimic Year</span>
            
          </v-flex>
          <v-flex xs12>
            <span>Price: $1500</span>
          </v-flex>
          </v-layout>
        </div>
        <v-card id="room-card" color="" light>
        <v-card-title primary-title>

          <v-layout class="room-card__quantity" wrap pa-3>

            <v-flex xs3>
              <h3>Total:</h3>
              <span>1250</span>
            </v-flex>

            <v-flex xs3>
              <h3>Total:</h3>
              <span>1250</span>
            </v-flex>

            <v-flex xs3>
              <h3>Avaliable:</h3>
              <span>20</span>
            </v-flex>

            <v-flex xs3>
              <h3>Reserved:</h3>
              <span>8</span>
            </v-flex>

          </v-layout>

        </v-card-title>
        <v-card-actions>
                <v-btn flat dark>Listen now</v-btn>
              </v-card-actions>
      </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>

    </v-layout> -->

  <v-layout wrap>

    <v-flex xs12 md12 v-for="n in 12" :key="n" pa-2>

      <v-card id="room-card" color="" light>
        <v-card-title primary-title>

          <v-flex class="room-card__title" xs12 md10>
            <h2>Single room</h2>
            <span>Full Acadimic Year</span>
          </v-flex>
          <!-- <v-flex xs12 md2>
            <h2>$1500</h2>
          </v-flex> -->

          <v-layout class="room-card__quantity" wrap>

            <v-flex xs3>
              <h3>Total Rooms:</h3>
              <span>1250</span>
            </v-flex>

            <v-flex xs3>
              <h3>Avaliable Rooms:</h3>
              <span>20</span>
            </v-flex>

            <v-flex xs3>
              <h3>Reserved Rooms:</h3>
              <span>8</span>
            </v-flex>

            <v-flex xs3>
              <h3>Qouta:</h3>
                <v-text-field v-model="name" :rules="nameRules" :counter="10" label="Name" required></v-text-field>
            </v-flex>

          </v-layout>

        </v-card-title>
        <v-card-actions>
          <v-btn flat dark>Listen now</v-btn>
        </v-card-actions>
      </v-card>

    </v-flex>

  </v-layout>

</div>
</template>

<script src="./ManageRooms.js"></script>

<style src="./ManageRooms.scss" lang="scss"></style>
