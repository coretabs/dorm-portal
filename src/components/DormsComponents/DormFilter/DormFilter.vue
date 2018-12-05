<template>
<div id="filter">
  <!-- filters sidebar -->
  <v-navigation-drawer touchless :clipped="$vuetify.breakpoint.lgAndUp" v-model="drawerControl" fixed app>
    <template>
      <div id="filters-heading">
        <v-icon left>filter_list</v-icon>{{lang.dormFilter.heading}} :
      </div>
      <div id="filters-body">

        <div class="filter" v-for="(filter,index) in filter.filters" :key="index">
          <div class="filter-title">{{filter.name}}</div>
          <template v-if="filter.checkbox">
            <ul>
              <li v-for="(option, index) in filter.options" :key="index">
                <v-checkbox :value="option.option_id" :label="option.name" color="success"></v-checkbox>
              </li>
            </ul>
          </template>
          <template v-if="filter.integral">
            <div>
              <v-layout class="integral-filter" row>
                <v-flex class="px-3">
                  <v-range-slider thumb-label="always" thumb-color="#3ab86c" v-model="filter.value" :max="filter.max_value" :min="filter.min_value" :step="1" color="success"></v-range-slider>
                </v-flex>
              </v-layout>
              <v-layout class="integral-filter" v-show="false" row>
                <v-flex class="integral-input">
                  <v-text-field label="From" v-model="filter.value[0]" class="mt-0" hide-details type="text" disabled></v-text-field>
                </v-flex>
                <v-flex class="integral-input">
                  <v-text-field label="To" v-model="filter.value[1]" class="mt-0" hide-details type="text" disabled></v-text-field>
                </v-flex>
              </v-layout>
            </div>
          </template>
        </div>
      </div>
    </template>
  </v-navigation-drawer>
  <v-content>
    <v-container id="rightside" fluid>
      <v-layout row wrap>

        <v-flex xs12>
          <dorm-search></dorm-search>
        </v-flex>
        
        <v-flex xs12>
          <!-- <div v-if="showAlert" class="search-noresult">
            <v-icon small>fa-exclamation-circle</v-icon>
            Sorry we didn't find any results matching this search
            <div class="close-alert"><v-icon small @click="showAlert = false">fa-times</v-icon></div>
          </div> -->
          <div v-if="showAlert" class="search-success">
            <v-icon small>fa-check-circle</v-icon>
            25 results matches your search
            <div class="close-alert"><v-icon small @click="showAlert = false">fa-times</v-icon></div>
          </div>
        </v-flex>

        <v-flex xs12>
          <dorm-card :dorm="dorm" v-for="(dorm,index) in dorms" :key="index"></dorm-card>
        </v-flex>

      </v-layout>
    </v-container>
  </v-content>
</div>
</template>

<script src="./DormFilter.js"></script>

<style src="./DormFilter.scss" lang="scss"></style>
