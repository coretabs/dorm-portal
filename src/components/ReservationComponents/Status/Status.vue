<template>
<v-layout id="status-step" row wrap>

  <v-flex xs12 md6>
    <v-layout row>
      <v-flex xs12 md6 class="status-row">
        <h3>{{lang.reservationStatus.statusHeading}}:</h3>
            <span><v-progress-circular
          indeterminate
          size="18"
          color="#ccc"
          v-if="reservation.status == 0"
        ></v-progress-circular>
        <v-icon v-if="reservation.status != 0">{{statusIcon}}</v-icon>
        {{status}}</span>
      </v-flex>
      <v-flex xs12 md6  class="status-row">
        <h3>Updated on:</h3>
      <span>{{reservation.last_update_date}}</span>
      </v-flex>
    </v-layout>
    <div>

    </div>

    <div class="status-row">
      <h3>{{lang.reservationStatus.commentHeading}}:</h3>
      <span v-if="reservation.status == 3 && !reservation.follow_up_message">Wating for dorm manager action.</span>
      <span v-if="reservation.status == 5 && !reservation.follow_up_message">Your reservation has expired.</span>
      <span v-else>{{reservation.follow_up_message}}</span>
    </div>

    <div class="status-row" v-if="reservation.status == 4">
      <h3>Submition Deadline:</h3>
      <span>{{reservation.confirmation_deadline_date}}</span>
    </div>

    <div class="status-button" v-if="reservation.status == 4">
      <v-btn dark color="#1c3a70" class="elevation-0" @click="$store.state.reservationStep = 2">
        <v-icon small>fa-cloud-upload-alt</v-icon>
        {{lang.reservationStatus.newUpload}}
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
      <v-flex xs12 id="bank-accounts" class="mt-0" v-if="reservation.status == 4">
        <h3>Our Bank Accounts:</h3>
        <v-expansion-panel>
          <v-expansion-panel-content v-for="(account,i) in reservation.room_characteristics.dormitory.bank_accounts" :key="i">
            <div slot="header">
              <v-icon class="v-icon__bank" small>fa-university</v-icon> {{account.bank_name}}
            </div>
            <v-card>
              <v-card-text>
                <table>
                  <tr>
                    <td><strong>Account name:</strong></td>
                    <td>{{account.account_name}}</td>
                  </tr>
                  <tr>
                    <td><strong>Currency:</strong></td>
                    <td>{{account.currency_code}}</td>
                  </tr>
                  <tr>
                    <td><strong>Account No:</strong></td>
                    <td>{{account.account_number}}</td>
                  </tr>
                  <tr>
                    <td><strong>swift:</strong></td>
                    <td>{{account.swift}}</td>
                  </tr>
                  <tr>
                    <td><strong>IBAN:</strong></td>
                    <td>{{account.iban}}</td>
                  </tr>
                </table>
              </v-card-text>
            </v-card>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-flex>
      <v-flex xs12 class="uploaded-file" v-if="reservation.receipts">
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
      </v-flex>
    </v-layout>

  </v-flex>

</v-layout>
</template>

<script src="./Status.js"></script>

<style src="./Status.scss" lang="scss"></style>
