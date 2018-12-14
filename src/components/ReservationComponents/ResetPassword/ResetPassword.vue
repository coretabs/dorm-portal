<template>
<v-content id="reset-password">
  <v-container fluid fill-height>
    <v-layout mt-5 justify-center>
      <v-flex xs12 sm8 md4>

        <v-card class="elevation-3 py-4" v-if="!isPasswordChanged">
          <v-card-text>

            <v-alert v-model="isError" dismissible type="error" class="mb-4">
              An error occured, please try again
            </v-alert>

            <h2 class="mb-3">Create a New Password</h2>
            <v-form ref="form" lazy-validation>
              <v-text-field label="New Password" v-model="password" :rules="passwordRules" required :append-icon="show ? 'visibility_off' : 'visibility'" @click:append="show = !show" :type="show ? 'text' : 'password'"></v-text-field>
              <v-text-field label="Repeat The Password" v-model="confirmPassword" :rules="[comparePasswords]" type="password"></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="#feae25" :disabled="!valid" large class="elevation-0" @click="submit">Reset Password</v-btn>
          </v-card-actions>
        </v-card>

        <v-card>
          <v-card-text class="pa-5" v-if="isPasswordChanged">
            <v-layout row wrap justify-center align-center>
              <v-flex xs12 class="text-xs-center mb-4">
                <v-icon class="success-icon">fa-check</v-icon>
              </v-flex>
              <v-flex xs12>
                <p class="success-text mb-1 text-xs-center">Your Password Has been changed successfully</p>
              </v-flex>
              <v-flex xs12 class="mt-4 text-xs-center">
                <v-btn color="#feae25" class="elevation-0" large to="/login">
                  Login now
                </v-btn>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>

      </v-flex>
    </v-layout>
  </v-container>
</v-content>
</template>

<script src="./ResetPassword.js"></script>

<style src="./ResetPassword.scss" lang="scss"></style>
