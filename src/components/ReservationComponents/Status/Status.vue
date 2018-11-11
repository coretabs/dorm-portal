<template>
<v-layout id="status-step" row wrap>
  <v-flex xs12 md4>
    <div class="uploaded-file">
      <v-list two-line subheader>
        <v-subheader inset>{{lang.reservationStatus.uploadedDocuments}}</v-subheader>
        <v-list-tile v-for="item in items" :key="item.title" avata>
          <v-list-tile-content>
            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
            <v-list-tile-sub-title>{{ item.subtitle }}</v-list-tile-sub-title>
          </v-list-tile-content>
          <!-- <v-list-tile-action>
                <v-btn icon>
                  <v-icon color="#606060">fa-eye</v-icon>
                </v-btn>
              </v-list-tile-action> -->
        </v-list-tile>
      </v-list>
      <v-btn color="#feae25" class="elevation-0" @click="e1 = 2">{{lang.reservationStatus.newUpload}}</v-btn>
    </div>
  </v-flex>
  <v-flex xs12 md8>
    <div class="status-row">
      <h3>{{lang.reservationStatus.statusHeading}}:</h3>
      <span><v-icon>fa-spinner</v-icon> Pending</span>
    </div>
    <div class="status-row">
      <h3>{{lang.reservationStatus.commentHeading}}:</h3>
      <span>Your payment is being reviewed.</span>
    </div>
    <div class="status-row">
      <h3>{{lang.reservationStatus.submittedHeading}}:</h3>
      <span>17/08/2018</span>
    </div>
  </v-flex>
</v-layout>
</template>

<script src="./Status.js"></script>

<style src="./Status.scss" lang="scss"></style>
