<template>
<v-content id="login">
  <v-container fluid fill-height>
    <v-layout mt-5 justify-center>
      <v-flex xs12 sm8 md4>
        <v-card class="elevation-3">
          <v-form ref="form" lazy-validation>
            <v-toolbar color="#fff" class="elevation-0">
              <v-toolbar-title>{{lang.login.heading}}</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <div v-for="(error,i) in errors" :key="i" class="mb-1">
                <p class="error-message" v-for="(err,i) in error" :key="i">
                  {{err}}
                </p>
              </div>
              <v-text-field prepend-icon="fa-envelope" :label="lang.login.email" v-model="email" :rules="emailRules" type="email" autofocus required></v-text-field>
              <v-text-field prepend-icon="fa-key" :label="lang.login.password" v-model="password" :append-icon="show ? 'visibility_off' : 'visibility'" @click:append="show = !show" :type="show ? 'text' : 'password'" required></v-text-field>
            </v-card-text>
            <v-card-actions>
              <a href="#" @click.stop="isForgotPassword" class="grey--text text--darken-2 forgot-link">{{lang.login.forgotPass}}?</a>
              <v-spacer></v-spacer>
              <v-btn color="#feae25" large class="elevation-0" @click.prevent="submit">{{lang.login.button}}</v-btn>
            </v-card-actions>
          </v-form>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
  <v-dialog v-model="forgotPassword" max-width="600" lazy>
    <v-card>

      <v-card-text class="px-4 py-5" v-if="!emailSent">
        <v-alert v-model="isEmailNotExist" dismissible type="error" class="mb-4">
          {{lang.resetPassword.notUser}}
        </v-alert>
        <h2 class="mb-3">{{lang.resetPassword.heading}}</h2>
        <v-form ref="form" lazy-validation>
          <v-text-field :label="lang.signup.email" autocomplete="on" :rules="emailRules" required type="email" v-model.trim="email" :disabled="emailSent"></v-text-field>
        </v-form>
      </v-card-text>

      <v-card-text class="pa-5" v-if="emailSent">
        <v-layout row wrap justify-center align-center>
          <v-flex xs12 class="text-xs-center mb-4">
            <v-icon class="success-icon">fa-envelope-open-text</v-icon>
          </v-flex>
          <v-flex xs12>
            <p class="success-text mb-1 text-xs-center">
              {{lang.resetPassword.successReset}}
            </p>
            <p class="success-text text-xs-center">{{lang.resetPassword.emailSent}}.</p>
          </v-flex>
          <v-flex xs12 class="mt-4 text-xs-center">
            <v-btn color="#feae25" class="elevation-0" large @click="forgotPassword = false">
              {{lang.shared.close}}
            </v-btn>
          </v-flex>
        </v-layout>
      </v-card-text>

      <v-card-actions v-if="!emailSent">
        <v-spacer></v-spacer>

        <v-btn color="gray darken-1" flat="flat" large @click="forgotPassword = false">
          {{lang.shared.cancel}}
        </v-btn>

        <v-btn color="#feae25" :disabled="!valid" class="elevation-0" large @click="resetPassword">
          {{lang.resetPassword.reset}}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</v-content>
</template>

<script src="./Login.js"></script>

<style src="./Login.scss" lang="scss"></style>
