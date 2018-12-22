<template>
<v-layout id="status-step" row wrap>
  
  <v-flex xs12 md6>
    <div class="status-row">
      <h3>{{lang.reservationStatus.statusHeading}}:</h3>
      <span><v-progress-circular
      indeterminate
      size="18"
      color="#ccc"
      v-if="reservation.status == 0"
    ></v-progress-circular>
      <v-icon v-if="reservation.status != 0">{{statusIcon}}</v-icon>
     {{status}}</span>
    </div>

    <div class="status-row" v-if="reservation.status == 5 || !!reservation.last_update_date ">
      <h3>Last Updated on:</h3>
      <span v-if="reservation.status == 5">{{reservation.confirmation_deadline_date}}</span>
      <span v-else>{{reservation.last_update_date}}</span>
    </div>

    <div class="status-row">
      <h3>{{lang.reservationStatus.commentHeading}}:</h3>
      <span v-if="reservation.status == 5">Your reservation has expired since you haven't uploaded the payment receipt before the deadline. You can contact the dorm manager or reserve a new room.</span>
      <span v-if="reservation.status == 0 && !reservation.follow_up_message">You receipt has been sent and is under review.</span>
      <span v-if="reservation.status == 3">Wating for dorm manager action.</span>
      <span v-if="reservation.status == 2">Congaraltion! your reservation is confirmed.</span>
      <span v-else>{{reservation.follow_up_message}}</span>
    </div>
    <div class="status-button" v-if="reservation.status == 0">
      <v-btn dark color="#1c3a70" class="elevation-0" @click="$store.state.reservationStep = 2">
        <v-icon small>fa-cloud-upload-alt</v-icon>
        {{lang.reservationStatus.newUpload}}</v-btn>
    </div>
    <div class="status-button" v-if="reservation.status == 5">
      <v-btn dark color="#1c3a70" class="elevation-0" @click="$store.state.reservationStep = 2">
        reserve new room
      </v-btn>
    </div>
  </v-flex>

  <v-flex xs12 md6>
    <div class="uploaded-file mt-2" v-if="reservation.receipts">
      <v-list two-line subheader>
        <v-subheader inset>{{lang.reservationStatus.uploadedDocuments}}</v-subheader>
        <v-list-tile v-for="(file,i) in reservation.receipts" :key="i" v-if="reservation.receipts.length > 0">
          <v-list-tile-content>
            <v-list-tile-title>
              <a :href="file.url" target="_blank" download class="grey--text text--darken-2">Reciept {{i}}</a>
            </v-list-tile-title>
            <v-list-tile-sub-title>{{ file.upload_receipt_date }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile v-if="reservation.receipts.length == 0">
          <v-list-tile-content>
            <v-list-tile-title>
              There are no files
            </v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </div>
  </v-flex>

</v-layout>
</template>

<script src="./Status.js"></script>

<style src="./Status.scss" lang="scss"></style>
