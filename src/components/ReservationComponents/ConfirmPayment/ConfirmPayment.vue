<template>
<v-layout row wrap class="mt-4">
  <v-flex v-if="isNewUpload" xs12 class="mx-3 pa-0 text-xs-right">
    <v-spacer></v-spacer>
    <v-btn color="#feae25" depressed class="upload-btn mb-4 mx-0" @click="nextStep">
      {{lang.confirmPayment.backToStatusBtn}}
      <v-icon small right>fa-arrow-right</v-icon>
    </v-btn>
  </v-flex>
  <v-flex v-if="date  && thereIsDeadline" xs12 class="mb-4 mx-3  confirmation-countdown">

    <h1>{{lang.confirmPayment.deadlineHeading}}</h1>

    <div class="hint">
      <v-tooltip bottom max-width="200">
        <v-icon color="#ccc" slot="activator">fa-question-circle</v-icon>
        <span>{{lang.confirmPayment.deadlineHint}}</span>
      </v-tooltip>
    </div>

    <flip-countdown :deadline="date"></flip-countdown>
  </v-flex>

  <v-flex xs12 md4 px-3 v-if="reservation.room_characteristics">
    <div id="amount" v-if="!isNewAmount">
      <h3>{{lang.confirmPayment.amountHeading}}:</h3>
      <span>{{reservation.room_characteristics.price_currency}}{{reservation.room_characteristics.price}}</span>
      <v-icon>fa-money-bill-alt</v-icon>
    </div>
    <div id="bank-accounts">
      <h3>{{lang.confirmPayment.bankAccountsHeading}}:</h3>
      <v-expansion-panel>
        <v-expansion-panel-content v-for="(account,i) in reservation.room_characteristics.dormitory.bank_accounts" :key="i">
          <div slot="header">
            <v-icon class="v-icon__bank" small>fa-university</v-icon> {{account.bank_name}}
          </div>
          <v-card>
            <v-card-text>
              <table>
                <tr>
                  <td><strong>{{lang.confirmPayment.accountName}}:</strong></td>
                  <td>{{account.account_name}}</td>
                </tr>
                <tr>
                  <td><strong>{{lang.confirmPayment.currency}}:</strong></td>
                  <td>{{account.currency_code}}</td>
                </tr>
                <tr>
                  <td><strong>{{lang.confirmPayment.accountNumber}}:</strong></td>
                  <td>{{account.account_number}}</td>
                </tr>
                <tr>
                  <td><strong>{{lang.confirmPayment.swift}}:</strong></td>
                  <td>{{account.swift}}</td>
                </tr>
                <tr>
                  <td><strong>{{lang.confirmPayment.iban}}:</strong></td>
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

          <div class="files-uploader">
            <v-form enctype="multipart/form-data" @submit.prevent="submit(reservation.id)">

              <div class="upload">

                <v-layout align-center wrap>
                  <v-flex md3 xs12>
                    <label for="file">
                      <v-icon>fa-plus</v-icon>
                      {{lang.confirmPayment.chooseFile}}
                    </label>
                  </v-flex>
                  <v-flex md9 xs12 class="text-md-left">
                    <p>{{lang.confirmPayment.allowedDocs}}: JEPG, PNG, GIF</p>
                  </v-flex>
                </v-layout>

                <input type="file" id="file" multiple @change="selectFile" ref="files" v-show="false">

              </div>
              <v-flex :class="`files-list ${file.invalidMessage && 'file-invalid'}`" v-for="(file,index) in files" :key="index" md12>
                <v-layout>
                  <v-flex class="text-truncate" md4>
                    <span>{{file.name}}</span>
                  </v-flex>
                  <v-flex class="text-md-center" md2>
                    <span>{{file.size/1000}} KB</span>
                  </v-flex>

                  <v-flex class="text-md-center" md5>
                    <span>{{file.invalidMessage}}</span>
                  </v-flex>
                  <v-flex class="text-md-right" md1>
                    <v-icon small @click="removeFile(index)">fa-times-circle</v-icon>
                  </v-flex>
                </v-layout>

              </v-flex>
              <v-btn type="submit" class="upload-btn mt-3" depressed v-show="this.files.length" color="#1c3a70" :dark="!disabled" :disabled="disabled" :loading="loadingBtn">{{lang.shared.submit}}</v-btn>
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
