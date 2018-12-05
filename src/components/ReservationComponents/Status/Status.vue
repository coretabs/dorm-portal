<template>
<v-layout id="status-step" row wrap>
  
  <v-flex xs12 md6>
    <div class="status-row">
      <h3>{{lang.reservationStatus.statusHeading}}:</h3>
      <span><v-progress-circular
      indeterminate
      size="18"
      color="#ccc"
    ></v-progress-circular> Pending</span>
    </div>
    <div class="status-row">
      <h3>{{lang.reservationStatus.commentHeading}}:</h3>
      <span>Your payment is being reviewed.</span>
    </div>
    <div class="status-button">
      <v-btn dark color="#1c3a70" class="elevation-0" @click="$store.state.reservationStep = 2">
        <v-icon small>fa-cloud-upload-alt</v-icon>
        {{lang.reservationStatus.newUpload}}</v-btn>
    </div>
  </v-flex>

  <v-flex xs12 md6>
    <div class="uploaded-file">
      <v-list two-line subheader>
        <v-subheader inset>{{lang.reservationStatus.uploadedDocuments}}</v-subheader>
        <v-list-tile v-for="item in items" :key="item.title" avata>
          <v-list-tile-content>
            <v-list-tile-title>
              <a href="#" class="grey--text text--darken-2">{{ item.title }}</a>
            </v-list-tile-title>
            <v-list-tile-sub-title>{{ item.subtitle }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </div>
  </v-flex>

</v-layout>
</template>

<script src="./Status.js"></script>

<style src="./Status.scss" lang="scss"></style>
