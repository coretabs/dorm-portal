<template>
<div id="manage-rooms" class="mb-5">
  <v-layout wrap>
    <v-btn color="success" dark medium fixed bottom right fab @click="loadComponent('AddNewRoom')">
      <v-icon>add</v-icon>
    </v-btn>

    <v-flex xs12 v-for="(room,i) in rooms" :key="i">
      <v-card id="room-card" class="mb-2">
        <v-menu bottom left class="room-card__actions absolute-menu">
          <v-btn slot="activator" icon>
            <v-icon>more_vert</v-icon>
          </v-btn>
          <v-list>
            <v-list-tile @click="editRoom(room.id)">
              <v-list-tile-title>
                <v-icon small left class="pr-2 green--text text--lighten-1">fa-edit</v-icon>
                Edit
                </v-list-tile-title>
            </v-list-tile>
            <v-list-tile @click="deleteRoom(room.id)">
              <v-list-tile-title>
                <v-icon small left class="pr-2 red--text text--lighten-1">fa-trash</v-icon>
                Delete
              </v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-menu>
        <v-card-title primary-title>
          <v-flex class="room-card__title" xs12 md3 px-3>
            <v-layout wrap>
              <v-flex class="room-card__title mb-2" xs12 md8>
                <h3>Room Type:</h3>
                <span>{{ room.room_type }}</span>
              </v-flex>
              <v-flex class="room-card__title" xs12 md4>
                <h3>availability:</h3>
                  <v-switch color="success" v-model="room.is_ready" @change="updateRoomStatus(room.id, room.is_ready)"></v-switch>

              </v-flex>
            </v-layout>
          </v-flex>

          <v-flex class="room-card__title" xs12 md8>
            <v-layout class="room-card__quantity" wrap>
              <v-flex xs12 sm6 md10>
                <h3>Reserved Rooms:</h3>
                <v-layout row wrap>
                  <v-flex xs12 md2>
                    <span>{{ room.reserved_rooms_number }}<sub>/{{ room.total_quota }}</sub></span>
                  </v-flex>
                  <v-flex xs12 md10>
                    <v-progress-linear class="room-card__progress" :color="progressColor(room.allowed_quota, room.total_quota,  room.reserved_rooms_number)" height="25" :value="progressValue(room.reserved_rooms_number, room.total_quota)"></v-progress-linear>
                  </v-flex>
                </v-layout>
              </v-flex>

              <v-flex xs12 sm6 md2>
                <h3>Quota:</h3>
                <v-layout row>
                  <span :class="quotaTextColor(room.allowed_quota, room.total_quota, room.reserved_rooms_number)">{{ room.allowed_quota }}</span>
                  <v-btn icon class="quota-update" dark @click="showQuotaUpdate(room.reserved_rooms_number, room.total_quota, room.allowed_quota, room.id)">
                    <v-icon small>fa-pencil-alt</v-icon>
                  </v-btn>
                </v-layout>
              </v-flex>

            </v-layout>
          </v-flex>
        </v-card-title>
      </v-card>
    </v-flex>

    <v-dialog v-model="deleteDialog.show" width="500" lazy>
      <v-card>
        <v-card-title class="headline text-uppercase font-weight-medium red accent-4 white--text">
          Confirm Delete
        </v-card-title>
        <v-card-text class="subheading my-3">
          <span>
            Are You sure you want to delete this room?
          </span>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="elevation-0" @click="deleteDialog.show = false">Cancel</v-btn>
          <v-btn color="red" class="elevation-0" @click="confirmDeleteRoom" :loading="loadingBtn">Delete Room</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showQuotaUpdatedialog" persistent max-width="350" lazy>
      <v-card>
        <v-card-text>
          <h2>Update Quota:</h2>
          <p v-if=" availableRooms(reservedRoomsNumber, totalRoomsNumber) > 0 " class="avaliable-quota__info">You can add upto <strong>{{  availableRoomsNumber }}</strong> room</p>
          <p v-else class="avaliable-quota__warning">You have <strong>0</strong> room to add</p>
          <v-text-field v-model="allowedQuotaNumber" type="number" min="0" :max="availableRoomsNumber" required :disabled="availableRoomsNumber == 0"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat @click="showQuotaUpdatedialog = false">Cancel</v-btn>
          <v-btn v-if="availableRoomsNumber > 0" color="green darken-1" flat @click="UpdateQuotaNumber">Confirm</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>


    <v-dialog v-model="showEditRoomDialog" fullscreen hide-overlay transition="dialog-bottom-transition" scrollable lazy>
      <v-card>
        <v-toolbar card dark color="#1c3a70">
          <v-toolbar-title>Edit Room</v-toolbar-title>
        </v-toolbar>
        <v-card-text class="pa-0">
          <edit-room :roomData="roomDetails" :roomId="roomEditId" @closeEditDialog="closeEditDialog($event)"></edit-room>
        </v-card-text>
      </v-card>
    </v-dialog>

  </v-layout>
</div>
</template>

<script src="./ManageRooms.js"></script>

<style src="./ManageRooms.scss" lang="scss"></style>
