<template>
<v-content id="reservation">
  <v-container fluid fill-height>
    <v-layout justify-center>
      <v-flex xs12 sm8 md8>
        <v-stepper v-model="reservationStep">
          <v-stepper-header class="elevation-3">
            <v-stepper-step :complete="e1 > 1" step="1" color="#1c3a70">Signup</v-stepper-step>

            <v-divider></v-divider>

            <v-stepper-step :complete="e1 > 2" step="2" color="#1c3a70">Confirm Payment</v-stepper-step>

            <v-divider></v-divider>

            <v-stepper-step step="3" color="#1c3a70">Await Approval</v-stepper-step>
          </v-stepper-header>

          <v-stepper-items>

            <v-stepper-content step="1">
              <sign-up></sign-up>
            </v-stepper-content>

            <v-stepper-content step="2">
              <confirm-payment></confirm-payment>

            </v-stepper-content>

            <v-stepper-content step="3">
              <reservation-status></reservation-status>
            </v-stepper-content>

          </v-stepper-items>
        </v-stepper>
      </v-flex>

    </v-layout>
  </v-container>
</v-content>
</template>

<script src="./ReservationProcess.js"></script>
<style src="./ReservationProcess.scss" lang="scss"></style>
