<template>
<div id="signup">

  <v-card class="elevation-0">
    <v-form action="#" @submit.prevent="login">
      <v-card-text>

        <v-text-field :label="lang.signup.email" type="email"></v-text-field>
        <v-text-field :label="lang.signup.password" :append-icon="show ? 'visibility_off' : 'visibility'" @click:append="show = !show" :type="show ? 'text' : 'password'"></v-text-field>

      </v-card-text>
      <v-card-actions>
        <a href="#" @click.stop="showSignup = !showSignup" class="grey--text text--darken-2 signup-link">{{lang.login.newAccount}}</a>
        <v-spacer></v-spacer>
        <v-btn type="submit" color="#feae25" class="elevation-0">{{lang.login.button2}}</v-btn>
      </v-card-actions>
    </v-form>
  </v-card>

  <v-dialog v-model="showSignup" width="500">
    <v-card class="elevation-0 card-padding">
      <v-card-text>
        <h2>{{lang.signup.heading}}</h2>
        <v-form>
          <v-text-field :label="lang.signup.firstName" type="text"></v-text-field>
          <v-text-field :label="lang.signup.lastName" type="text"></v-text-field>
          <v-text-field :label="lang.signup.passport" type="text"></v-text-field>
          <v-text-field :label="lang.signup.email" type="email"></v-text-field>
          <v-text-field :label="lang.signup.password" :append-icon="show ? 'visibility_off' : 'visibility'" @click:append="show = !show" :type="show ? 'text' : 'password'"></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="#feae25" large class="elevation-0">{{lang.signup.button}}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

</div>
</template>

<script src="./Signup.js"></script>

<style src="./Signup.scss" lang="scss"></style>
