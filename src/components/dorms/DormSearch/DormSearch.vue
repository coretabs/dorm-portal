<template>
<v-form id="search-dorm">
  <h2>{{lang.dormSearch.heading}}</h2>
  <v-layout row wrap>
    <v-flex xs12 sm3>
      <v-select :items="DormsType" label="Dormitories type" prepend-inner-icon="meeting_room" solo color="success" append-icon="expand_more" :menu-props="{
            offsetY: '',
            transition: 'slide-y-transition',
            bottom: ''
          }" v-model="defaultDormType"></v-select>
    </v-flex>
    <v-flex xs12 sm2>
      <v-select class="shift-left" :items="AcademicYear" label="Duration" prepend-inner-icon="calendar_today" solo color="success" append-icon="expand_more" :menu-props="{
            offsetY: '',
            transition: 'slide-y-transition',
            bottom: ''
          }" v-model="defaultAcademicYear"></v-select>
    </v-flex>
    <v-flex xs12 md1>
      <v-btn depressed large>
        <v-icon>fa-search</v-icon>{{lang.dormSearch.button}}
      </v-btn>
    </v-flex>
  </v-layout>
</v-form>
</template>

<script  src="./DormSearch.js"></script>

<style src="./DormSearch.scss" lang="scss"></style>
