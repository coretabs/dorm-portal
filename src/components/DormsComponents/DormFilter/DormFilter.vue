<template>
<div id="filter">
  <!-- filters sidebar -->
  <v-navigation-drawer touchless :clipped="$vuetify.breakpoint.lgAndUp" v-model="drawerControl" fixed app>
    <template>
      <div id="filters-heading">
        <v-icon left>fa-filter</v-icon>{{lang.dormFilter.heading}} :
      </div>
      <div id="filters-body">
        <div class="loading-progress" v-if="loadingFilters">
          <v-progress-circular
            :size="50"
            color="grey"
            indeterminate
          ></v-progress-circular>
        </div>
        <div v-if="!loadingFilters" class="filter">
          <div class="filter-title">{{lang.dormFilter.dormFeatures}}:</div>
          <template>
            <ul>
              <li v-for="(dormFeature, index) in filters.dorm_features" :key="index">
                <v-checkbox v-model="dormSelectedFeatures" @change="dormFeatiresFilter" :value="dormFeature.id" :label="dormFeature.name" color="success"></v-checkbox>
              </li>
            </ul>
          </template>
          <div class="filter-title">{{lang.dormFilter.roomFeatures}}:</div>
          <template>
            <ul>
              <li v-for="(roomFeatures, index) in filters.room_features" :key="index">
                <v-checkbox v-model="roomSelectedFeatures" @change="roomFeatiresFilter" :value="roomFeatures.id" :label="roomFeatures.name" color="success"></v-checkbox>
              </li>
            </ul>
          </template>
          <div v-for="(additionalFilters, i) in filters.additional_filters" :key="i">
            <div class="filter-title">{{additionalFilters.name}}</div>
            <template v-if="additionalFilters.is_checkbox">
              <ul>
                <li v-for="(option, index) in additionalFilters.options" :key="index">
                  <v-checkbox v-model="additionalFiltersHolder" @change="selectedAdditionalFilters(additionalFilters.id, option.id)" :value="option.id" :label="option.name" color="success"></v-checkbox>
                </li>
              </ul>
            </template>
            <template v-if="additionalFilters.is_integral">
              <div>
                <v-layout class="integral-filter" row wrap>
                  <v-flex xs12 class="px-2">
                    <v-range-slider @change="integralFilter(additionalFilters.value, additionalFilters.id)" thumb-color="#3ab86c" v-model="additionalFilters.value" :max="additionalFilters.max_value" :min="additionalFilters.min_value" :step="1" color="success"></v-range-slider>
                  </v-flex>
                  <v-flex xs12 class="mb-3 text-xs-center font-weight-medium">
                    <span>{{additionalFilters.value[0]}} - {{additionalFilters.value[1]}}</span>
                  </v-flex>
                </v-layout>
                <v-layout class="integral-filter" v-show="false" row>
                  <v-flex class="integral-input">
                    <v-text-field label="From" v-model="additionalFilters.value[0]" class="mt-0" hide-details type="text" disabled></v-text-field>
                  </v-flex>
                  <v-flex class="integral-input">
                    <v-text-field label="To" v-model="additionalFilters.value[1]" class="mt-0" hide-details type="text" disabled></v-text-field>
                  </v-flex>
                </v-layout>
              </div>
            </template>
          </div>
        </div>
      </div>
    </template>
  </v-navigation-drawer>
  <v-content>
    <v-container id="rightside" fluid>
      <v-layout row wrap>

        <v-flex xs12>
          <dorm-search :dutarion="setDuration" :category="setCategory"></dorm-search>
        </v-flex>

        <v-flex xs12>
          <div v-if="resultAlert > 0" class="search-success">
            <v-icon small>fa-check-circle</v-icon>
            {{resultAlert}}
            <span v-if="resultAlert > 1">
              {{lang.dormFilter.dorms}} {{lang.dormFilter.searchResult}}
            </span>
            <span v-else>
              {{lang.dormFilter.dorm}} {{lang.dormFilter.searchResult}}
            </span>
          </div>
          <div v-if="resultAlert == 0" class="search-noresult">
            <v-icon small>fa-exclamation-circle</v-icon>
             {{lang.dormFilter.noSearchResult}} {{lang.dormFilter.searchResult}}
          </div>
        </v-flex>
        
        <v-flex xs12 v-if="loadingDorms" class="text-xs-center">
          <v-progress-circular
            :size="50"
            color="grey"
            indeterminate
          ></v-progress-circular>
        </v-flex>

        <v-flex xs12 v-if="!loadingDorms">
          <dorm-card :dorm="dorm" v-for="(dorm,index) in dorms" :key="index"></dorm-card>
        </v-flex>

      </v-layout>
    </v-container>
  </v-content>
</div>
</template>
<script src="./DormFilter.js"></script>
<style src="./DormFilter.scss" lang="scss"></style>
