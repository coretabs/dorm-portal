<template>
<div id="manage-reservations" class="text-xs-center">
  <h1 class="my-5">Choose Dorm To Manage</h1>
  <v-layout wrap row justify-center>
    <v-flex md4 xs12 v-for="(dorm,index) in dorms" :key="index">
      <v-card class="ma-3">
        <v-img :src="dorm.cover" aspect-ratio="2.75" gradient="to top right, rgba(44,40,72,.4), rgba(44,40,72,.4)">
          <v-layout slot="placeholder" fill-height align-center justify-center ma-0>
            <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
          </v-layout>
        </v-img>

        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-0">{{dorm.name}}</h3>
          </div>
        </v-card-title>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="orange" @click="chosenDorm(dorm.id)">Manage</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>

</div>
</template>

<script src="./SelectDorm.js"></script>

<style src="./SelectDorm.scss" lang="scss"></style>
