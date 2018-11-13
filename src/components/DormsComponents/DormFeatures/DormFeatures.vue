<template>
<v-container id="all-features" grid-list-sm>
  <v-layout row wrap>
    <v-flex xs12>
      <h2>{{dormName}} {{lang.dormCard.features}}:</h2>
    </v-flex>
    <v-flex xs12>
      <div class="dorm-feature" v-for="(feature,index) in features" :key="index">
        <v-icon>{{feature.icon}}</v-icon>
        <span>{{feature.name}}</span>
      </div>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script  src="./DormFeatures.js"></script>

<style src="./DormFeatures.scss" lang="scss"></style>
