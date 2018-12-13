<template>
<v-content id="confirm-account">
  <v-container fluid fill-height>
    <v-layout mt-5 justify-center>
      <v-flex xs12 sm8 md6>

        <v-card class="elevation-3 py-5" v-if="isConfirmed">

          <v-card-text>
            <v-layout row wrap justify-center align-center>
              <v-flex xs12 class="text-xs-center mb-4">
                <v-icon class="success-icon">fa-check</v-icon>
              </v-flex>
              <v-flex xs12>
                <p class="success-text text-xs-center">Your Email has been confirmed</p>
                <p class="success-text text-xs-center">You can now complate your reservation process</p>
              </v-flex>
            </v-layout>
          </v-card-text>

          <v-layout justify-center class="mt-4">
            <v-btn to="/login" color="#feae25" large class="elevation-0">Login to continue</v-btn>
          </v-layout>

        </v-card>

        <v-card class="elevation-3 pt-3 pb-5" v-else>

          <v-card-text>
            <v-layout row wrap justify-center align-center>
              <v-flex xs12>

                <v-alert v-model="alert" dismissible type="error">
                  The link you followed may have expired, please re-enter your Email below to get a new activation Email.
                </v-alert>

              </v-flex>
              <v-flex xs12 md6 class="mt-5 mb-1">
                <h2 class="mb-1">Resend Activation Email</h2>
                <v-form ref="form" :value="valid" lazy-validation>
                  <v-text-field :label="lang.signup.email" autocomplete="on" :rules="emailRules" required type="email" v-model.trim="email"></v-text-field>
                </v-form>
              </v-flex>
            </v-layout>
          </v-card-text>

          <v-layout justify-center>
            <v-flex xs12 md6 class="text-xs-right">
              <v-btn color="#feae25" large class="elevation-0">send</v-btn>
            </v-flex>
          </v-layout>

        </v-card>

      </v-flex>
    </v-layout>
  </v-container>
</v-content>
</template>

<script src="./ConfirmAccount.js"></script>

<style src="./ConfirmAccount.scss" lang="scss"></style>
