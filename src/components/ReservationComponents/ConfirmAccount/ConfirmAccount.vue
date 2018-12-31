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
                <p class="success-text text-xs-center">{{lang.confirmAccount.heading}}</p>
                <p class="success-text text-xs-center">
                  {{lang.confirmAccount.desc}}
                </p>
              </v-flex>
            </v-layout>
          </v-card-text>

          <v-layout justify-center class="mt-4">
            <v-btn to="/login" color="#feae25" large class="elevation-0">{{lang.confirmAccount.btn}}</v-btn>
          </v-layout>

        </v-card>

        <v-card class="elevation-3 pt-3 pb-5" v-if="isNotConfirmed">

          <v-card-text>
            <v-layout row wrap justify-center align-center>
              <v-flex xs12>

                <v-alert v-model="isExpiredLink" dismissible type="warning" class="black--text">
                  {{lang.confirmAccount.expiredLink}}.
                </v-alert>

                <v-alert v-model="isEmailNotExist" dismissible type="error">
                  {{lang.confirmAccount.notRegestered}}.
                </v-alert>

                <v-alert v-model="emailSent" dismissible type="success">
                  {{lang.confirmAccount.emailSent}}
                </v-alert>

              </v-flex>
              <v-flex xs12 md6 class="mt-5 mb-1">
                <h2 class="mb-1">{{lang.resendActivationEmail.heading}}</h2>
                <v-form ref="form" lazy-validation>
                  <v-text-field :label="lang.signup.email" autocomplete="on" :rules="emailRules" required type="email" v-model.trim="email" :disabled="emailSent"></v-text-field>
                </v-form>
              </v-flex>
            </v-layout>
          </v-card-text>

          <v-layout justify-center>
            <v-flex xs12 md6 class="text-xs-right">
              <v-btn color="#feae25" :disabled="!valid" large class="elevation-0" @click="submit">{{lang.resendActivationEmail.btn}}</v-btn>
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
