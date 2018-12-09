<template>
<v-content id="login">
  <v-container fluid fill-height>
    <v-layout mt-5 justify-center>
      <v-flex xs12 sm8 md4>
        <v-card class="elevation-3">
          <v-form action="#" @submit.prevent="submit">
            <v-toolbar color="#fff" class="elevation-0">
              <v-toolbar-title>{{lang.login.heading}}</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-text-field prepend-icon="fa-envelope" :label="lang.login.email" type="email"></v-text-field>
              <v-text-field prepend-icon="fa-key" :label="lang.login.password" :append-icon="show ? 'visibility_off' : 'visibility'" @click:append="show = !show" :type="show ? 'text' : 'password'"></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn type="submit" color="#feae25" large class="elevation-0">{{lang.login.button}}</v-btn>
            </v-card-actions>
          </v-form>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</v-content>
</template>

<script src="./Login.js"></script>

<style src="./Login.scss" lang="scss"></style>
