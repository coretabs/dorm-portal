<template>
<div id="signup">
  <v-card class="elevation-0">
    <v-card-text>
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
      <v-btn color="#feae25" large class="elevation-0" @click="e1 = 2">{{lang.signup.button}}</v-btn>
    </v-card-actions>
  </v-card>
</div>
</template>

<script src="./Signup.js"></script>

<style src="./Signup.scss" lang="scss"></style>
