<template>
<v-layout row wrap>
  <v-flex v-if="date" xs12 class="mb-5 mt-4 confirmation-countdown">
    <h1>Confirmation Deadline</h1>
    <flip-countdown :deadline="date"></flip-countdown>
  </v-flex>
  <v-flex xs12 md4 px-3 v-if="reservation.room_characteristics">
    <div id="amount">
      <h3>Amount to pay:</h3>
      <span>{{reservation.room_characteristics.price_currency}}{{reservation.room_characteristics.price}}</span>
      <v-icon>fa-money-bill-alt</v-icon>
    </div>
    <div id="bank-accounts">
      <h3>Our Bank Accounts:</h3>
      <v-expansion-panel>
        <!-- TODO: Add bank to DB -->
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
    </div>
  </v-flex>
  <v-flex xs12 md8 px-3>
    <div>
      <v-card class="elevation-0">
        <v-card-text class="pa-0">
          <p class="payment-instruction">
            <v-icon small>fa-exclamation-triangle</v-icon> {{lang.confirmPayment.instruction}}
          </p>

          <!-- <div class="drag-drop">
          <div class="upload">
            <v-form enctype="multipart/form-data">
              <label for="file">
                <v-icon>fa-plus</v-icon>
                {{lang.confirmPayment.chooseFile}}
              </label>
              <input type="file" id="file" @change="selectFile" ref="file" v-show="false"></input>
            </v-form>
          </div>
          </div> -->
          
          <div class="drag-drop">
            <v-form enctype="multipart/form-data" @submit.prevent="submit(reservation.id)">

              <div class="upload">

                <v-layout align-center>
                  <v-flex md3>
                    <label for="file">
                      <v-icon>fa-plus</v-icon>
                      {{lang.confirmPayment.chooseFile}}
                    </label>
                  </v-flex>
                  <v-flex md9 class="text-md-left">
                    <p>Drag &amp; drop your payment receipt here.</p>
                  </v-flex>
                </v-layout>

                <input type="file" id="file" @change="selectFile" ref="file" v-show="false"></input>

              </div>
              <v-btn type="submit">upload</v-btn>
            </v-form>

          </div>

        </v-card-text>

      </v-card>
    </div>
  </v-flex>

</v-layout>
</template>

<script src="./ConfirmPayment.js"></script>

<style src="./ConfirmPayment.scss" lang="scss"></style>
