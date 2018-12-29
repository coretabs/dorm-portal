<template>
<div id="manage-dorm">
  <v-card>
    <v-card-text>
      <v-form ref="form" lazy-validation>
        <v-layout wrap>

          <v-flex xs12 sm6 md4 pa-3>
            <h3 class="heading">General Spec:</h3>
            <v-select class="shift-left" :items="roomFilters.room_types" item-text="name" item-value="id" label="Room Type" append-icon="expand_more" :menu-props="{
            offsetY: '',
            transition: 'slide-y-transition',
            bottom: ''
          }" v-model="room.roomTypeId"></v-select>

            <v-select class="shift-left" :items="roomFilters.durations" item-text="name" item-value="id" label="Duration" append-icon="expand_more" :menu-props="{
            offsetY: '',
            transition: 'slide-y-transition',
            bottom: ''
          }" v-model="room.durationId"></v-select>

            <v-text-field label="Number of people" type="number" v-model="room.peopleAllowedNumber"></v-text-field>

            <v-layout wrap>
              <v-flex xs12 sm8>
                <v-text-field label="price" type="number" v-model="room.price"></v-text-field>
              </v-flex>
              <v-flex xs12 sm4 pl-2>
                <v-select class="shift-left" :items="roomFilters.currencies" v-model="room.currencyId" item-text="code" item-value="id" label="Currency" color="success" append-icon="expand_more" :menu-props="{
            offsetY: '',
            transition: 'slide-y-transition',
            bottom: ''
          }"></v-select>
              </v-flex>
            </v-layout>

            <v-text-field label="Total Rooms in Dorm" type="number" v-model="room.totalQuota"></v-text-field>
            <v-text-field label="Quota" type="number" v-model="room.allowedQuota"></v-text-field>
            <v-text-field label="Confirmation Duration in Days" type="number" v-model="room.confirmationDays"></v-text-field>
          </v-flex>

          <v-flex xs12 sm6 md4 pa-3>
            <h3 class="heading">Room Features:</h3>
            <v-autocomplete v-model="room.roomFeatures" :disabled="isUpdating" :items="roomFilters.room_features" box chips color="blue-grey lighten-2" label="Select features" item-text="name" item-value="id" multiple>
              <template slot="selection" slot-scope="data">
                <v-chip :selected="data.selected" close class="chip--select-multi" @input="remove(data.item)">
                  {{data.item.name}}
                </v-chip>
              </template>
              <template slot="item" slot-scope="data">

                <template>
                  <v-list-tile-content>
                    <v-list-tile-title v-html="data.item.name"></v-list-tile-title>
                  </v-list-tile-content>
                </template>
              </template>
            </v-autocomplete>

            <div v-for="(filter,i) in roomFilters.additional_filters" :key="i">

              <div v-if="filter.is_checkbox">
                <v-select class="shift-left" :items="filter.options" v-model="room.radioChoices[i]" item-text="name" item-value="id" :label="filter.name" append-icon="expand_more" :menu-props="{
                offsetY: '',
                transition: 'slide-y-transition',
                bottom: ''
              }"></v-select>

              </div>
              <div v-if="filter.is_integral">
                <v-text-field :label="filter.name" v-model="room.integralChoicesHolder[i]" @change="integralFilter(filter.id, i)" type="number"></v-text-field>
              </div>

            </div>

          </v-flex>

          <v-flex xs12 sm6 md4 pa-3>
            <h3 class="heading">Room Photos:</h3>

            <!-- upload files -->

          </v-flex>

          <v-flex xs12>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="#feae25" large class="elevation-0" @click="submitNewRoom">Add Room</v-btn>
            </v-card-actions>
          </v-flex>

        </v-layout>
      </v-form>
    </v-card-text>
  </v-card>
</div>
</template>

<script src="./AddNewRoom.js"></script>

<style src="./AddNewRoom.scss" lang="scss"></style>
