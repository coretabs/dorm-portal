<template>
<v-content id="reservation">
  <v-container fluid fill-height py-5>
    <v-layout justify-center>
      <v-flex xs12 sm8 md8>
        <v-stepper v-model="reservationStep" class="pb-4">
          <v-stepper-header class="elevation-3">
            <v-stepper-step :complete="progress > 1" step="1" color="#1c3a70">{{lang.reservationProcess.step1}}</v-stepper-step>

            <v-divider></v-divider>

            <v-stepper-step :complete="progress > 2" step="2" color="#1c3a70">{{lang.reservationProcess.step2}}</v-stepper-step>

            <v-divider></v-divider>

            <v-stepper-step :complete="reservationComplated" step="3" color="#1c3a70">{{lang.reservationProcess.step3}}</v-stepper-step>

          </v-stepper-header>

          <v-stepper-items>

            <v-stepper-content step="1">
              <sign-up></sign-up>
            </v-stepper-content>

            <v-stepper-content class="pt-0" step="2">
              <div v-if="!isRoomNotSaved && !isRoomReserved">
                <div class="noroom-alert mt-4">
                  <v-icon left>fa-info-circle</v-icon>
                  <span>{{lang.reservationProcess.noRoomSelected}}.</span>
                </div>
                <v-layout justify-center class="my-4">
                  <v-btn large dark color="#1c3a70" to="/">{{lang.reservationProcess.findRoomBtn}}</v-btn>
                </v-layout>
              </div>
              <confirm-payment v-else></confirm-payment>
            </v-stepper-content>

            <v-stepper-content step="3">
              <reservation-status></reservation-status>
            </v-stepper-content>

          </v-stepper-items>
        </v-stepper>
      </v-flex>

    </v-layout>
  </v-container>

  <v-tooltip top v-if="this.$store.getters.isLoggedIn">
    <v-btn slot="activator" color="rgb(36, 204, 27)" class="contact-icon" dark fab @click="contactDate">
      <v-icon>fa-comment-alt</v-icon>
    </v-btn>
    <span>{{lang.dormProfile.contactUs}}</span>
  </v-tooltip>

  <v-dialog v-model="contactDialog" max-width="500" lazy>
    <v-card>
      <v-card-text class="pa-4">
        <h2 class="mb-4">{{lang.reservationProcess.contactMsg}}:</h2>
        <div class="contact-info">
          <v-icon>fa-envelope</v-icon> <span>{{lang.dormProfile.contactEmail}}:</span> {{contact.contact_email}}
        </div>
        <div class="contact-info">
          <v-icon>fa-phone</v-icon> <span>{{lang.dormProfile.contactPhone}}:</span> {{contact.contact_number}}
        </div>
        <div class="contact-info">
          <v-icon>fa-fax</v-icon> <span>{{lang.dormProfile.ContactFax}}:</span> {{contact.contact_fax}}
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>

</v-content>
</template>

<script src="./ReservationProcess.js"></script>

<style src="./ReservationProcess.scss" lang="scss"></style>
