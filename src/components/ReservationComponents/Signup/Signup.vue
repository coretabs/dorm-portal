<template>
<div id="signup">

  <v-card class="elevation-0 card-padding" v-if="showRegisterForm">
    <v-card-text>
      <h2 class="mb-2">{{lang.signup.heading}}</h2>

      <div v-for="(error,i) in errors" :key="i">
        <p class="error-message" v-for="(err,i) in error" :key="i">
          {{err}}
        </p>
      </div>

      <v-form ref="form" lazy-validation>
        <v-text-field :label="lang.signup.firstName" autocomplete="on" :rules="nameRules" required type="text" v-model.trim="firstName"></v-text-field>
        <v-text-field :label="lang.signup.lastName" autocomplete="on" :rules="nameRules" required type="text" v-model.trim="lastName"></v-text-field>
        <v-text-field :label="lang.signup.email" autocomplete="on" :rules="emailRules" required type="email" v-model.trim="email"></v-text-field>
        <v-text-field :label="lang.signup.password" v-model="password" :rules="passwordRules" required :append-icon="show ? 'visibility_off' : 'visibility'" @click:append="show = !show" :type="show ? 'text' : 'password'"></v-text-field>
      </v-form>
      
    </v-card-text>
    <v-card-actions>
      <a href="#" @click.stop.prevent="redirectToLogin" class="grey--text text--darken-2 signup-link">{{lang.signup.haveAccount}}</a>
      <v-spacer></v-spacer>
      <v-btn color="#feae25" :disabled="!valid" large class="elevation-0" @click="submit">{{lang.signup.button}}</v-btn>
    </v-card-actions>
  </v-card>

  <div v-else class="mb-5 mt-5">
    <v-layout row wrap justify-center align-center>
      <v-flex xs12 class="text-xs-center mb-4">
        <v-icon class="success-icon">fa-check</v-icon>
      </v-flex>
      <v-flex xs12>
        <p class="success-text mb-1 text-xs-center">Your account has been successfully created.</p>
        <p class="success-text text-xs-center">An email has been sent to you with detailed instructions on how to activate it.</p>
      </v-flex>
      </v-layout>
  </div>

</div>
</template>

<script src="./Signup.js"></script>

<style src="./Signup.scss" lang="scss"></style>
