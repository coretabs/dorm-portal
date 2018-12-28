<template>
<v-layout id="status-step" row wrap>

  <v-flex xs12 md6>
    <v-layout row>
      <v-flex xs12 md6 class="status-row">
        <h3>{{lang.reservationStatus.statusHeading}}:</h3>
        <span>
          <v-progress-circular
            indeterminate
            size="18"
            color="#ccc"
            v-if="reservation.status == 3"
          ></v-progress-circular>
          <v-icon v-if="reservation.status != 3">{{statusIcon}}</v-icon>
          {{status}}
        </span>
      </v-flex>
      <v-flex xs12 md6 class="status-row">
        <h3>Updated on:</h3>
        <span>{{reservation.last_update_date}}</span>
      </v-flex>
    </v-layout>

    <div class="status-row message-block">
      <h3>{{lang.reservationStatus.commentHeading}}:</h3>
      <span v-if="reservation.status == 3">Wating for dorm manager action.</span>
      <span v-else-if="reservation.status == 5 && !reservation.follow_up_message">Your reservation has expired.</span>
      <span v-else>{{reservation.follow_up_message}}</span>
    </div>

    <div class="status-row" v-if="reservation.status == 4">
      <h3>Submition Deadline:</h3>
      <span>{{reservation.confirmation_deadline_date}}</span>
    </div>
    
    <div class="status-button" v-if="reservation.status == 3">
      <v-btn dark color="#1c3a70" class="elevation-0" @click="previousStep">
        <v-icon small left>fa-arrow-left</v-icon>
        Upload a receipt
      </v-btn>
    </div>
    
    <div class="status-button" v-if="reservation.status == 4">
       <v-btn dark class="elevation-0 theme--light success" @click="previousStep('required')">
        Submit receipt
      </v-btn>
    </div>

    <div class="status-button" v-if="reservation.status == 5">
      <v-btn dark color="#1c3a70" class="elevation-0" @click="$store.state.reservationStep = 2">
        reserve new room
      </v-btn>
    </div>
  </v-flex>

  <v-flex xs12 md6>
    <v-layout column class="pa-2">
      <v-flex xs12 class="uploaded-file" v-if="reservation.receipts">
        <v-list two-line subheader>
          <v-subheader inset>{{lang.reservationStatus.uploadedDocuments}}</v-subheader>
          <v-list-tile v-for="(file,i) in reservation.receipts" :key="i" v-if="reservation.receipts.length > 0">
            <v-list-tile-content>
              <v-list-tile-title>
                <a :href="file.url" target="_blank" download class="grey--text text--darken-2">Reciept {{i+1}}</a>
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
      </v-flex>
    </v-layout>

  </v-flex>

</v-layout>
</template>

<script src="./Status.js"></script>

<style src="./Status.scss" lang="scss"></style>
