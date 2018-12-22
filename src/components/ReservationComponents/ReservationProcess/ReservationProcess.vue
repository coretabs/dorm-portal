<template>
<v-content id="reservation">
  <v-container fluid fill-height mb-4 mt-3>
    <v-layout justify-center>
      <v-flex xs12 sm8 md8>
        <v-stepper v-model="reservationStep" class="pb-4">
          <v-stepper-header class="elevation-3">
            <v-stepper-step :complete="progress > 1" step="1" color="#1c3a70">Register</v-stepper-step>

            <v-divider></v-divider>

            <v-stepper-step :complete="progress > 2" step="2" color="#1c3a70">Confirm Payment</v-stepper-step>

            <v-divider></v-divider>

            <v-stepper-step :complete="complated" step="3" color="#1c3a70">Await Approval</v-stepper-step>

          </v-stepper-header>

          <v-stepper-items>

            <v-stepper-content step="1">
              <sign-up></sign-up>
            </v-stepper-content>

            <v-stepper-content class="pt-0" step="2">
              <div v-if="!isRoomNotSaved && !isRoomReserved">
                <div class="noroom-alert mt-4">
                  <v-icon left>fa-info-circle</v-icon>
                  <span>Ops! it seems that you haven't choosen any room yet.</span>
                </div>
                <v-layout justify-center class="my-4">
                  <v-btn large dark color="#1c3a70" to="/">Find your Room Now</v-btn>
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

  <v-tooltip top>
    <v-btn slot="activator" color="rgb(36, 204, 27)" class="contact-icon" dark fab>
      <v-icon>fa-comment-alt</v-icon>
    </v-btn>
    <span>Contact Us</span>
  </v-tooltip>

</v-content>
</template>

<script src="./ReservationProcess.js"></script>

<style src="./ReservationProcess.scss" lang="scss"></style>
