<template>
<div id="manage-dorm">
  <v-card class="mb-5">
    <v-card-text>
      <v-form ref="form" lazy-validation>
        <v-layout wrap>

          <v-flex xs12 sm6 md4 pa-3>
            <h2 class="heading">General Properties:</h2>
            <v-select class="shift-left" :items="roomFilters.room_types" :rules="requiredRules" item-text="name" item-value="id" label="Room Type" append-icon="expand_more" :menu-props="{
            offsetY: '',
            transition: 'slide-y-transition',
            bottom: ''
          }" v-model="room.roomTypeId"></v-select>

            <v-select class="shift-left" :items="roomFilters.durations" :rules="requiredRules" item-text="name" item-value="id" label="Duration" append-icon="expand_more" :menu-props="{
            offsetY: '',
            transition: 'slide-y-transition',
            bottom: ''
          }" v-model="room.durationId"></v-select>

            <v-text-field label="Number of people" type="number" :rules="requiredRules" v-model="room.peopleAllowedNumber"></v-text-field>

            <v-layout wrap>
              <v-flex xs12 sm8>
                <v-text-field label="price" type="number" :rules="requiredRules" v-model="room.price"></v-text-field>
              </v-flex>
              <v-flex xs12 sm4 pl-2>
                <v-select class="shift-left" :rules="requiredRules" :items="roomFilters.currencies" v-model="room.currencyId" item-text="code" item-value="id" label="Currency" color="success" append-icon="expand_more" :menu-props="{
                  offsetY: '',
                  transition: 'slide-y-transition',
                  bottom: ''
                }"></v-select>
              </v-flex>
            </v-layout>

            <v-text-field label="Total Rooms in Dorm" hint="Number of all rooms of this type in your dorm" :rules="requiredRules" type="number" v-model="room.totalQuota"></v-text-field>
            <v-text-field label="Quota" hint="Number of rooms you want to open for online reservation" type="number" :rules="requiredRules" v-model="room.allowedQuota"></v-text-field>
            <v-text-field label="Confirmation Duration in Days" hint="Give students a deadline to upload payment receipts" :rules="requiredRules" type="number" v-model="room.confirmationDays"></v-text-field>

            <v-autocomplete class="features-input" v-model="room.roomFeatures" :disabled="isUpdating" :items="roomFilters.room_features" box chips color="blue-grey lighten-2" label="Select features" item-text="name" item-value="id" multiple>
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
          </v-flex>

          <v-flex xs12 sm6 md4 pa-3>
            <h2 class="heading">Room Features:</h2>

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
            <h2 class="heading">Room Photos:</h2>

            <div class="files-uploader">
              <v-form enctype="multipart/form-data">
                <div class="upload">
                  <v-layout align-center wrap>
                    <v-flex md4 xs12>
                      <label for="file">
                        <v-icon>fa-plus</v-icon>
                        {{lang.confirmPayment.chooseFile}}
                      </label>
                    </v-flex>
                    <v-flex md8 xs12 class="text-md-left">
                      <p>Allowed documents: JEPG, PNG, GIF</p>
                    </v-flex>
                  </v-layout>
                  <input type="file" id="file" multiple @change="selectFile" ref="files" v-show="false">
                </div>
                  <v-flex :class="`files-list ${file.invalidMessage && 'file-invalid'}`" v-for="(file,index) in files" :key="index" md12>
                    <v-layout>
                      <v-flex class="text-truncate" md4>
                        <span>{{file.name}}</span>
                      </v-flex>
                      <v-flex class="text-md-center" md2>
                        <span>{{file.size/1000}} KB</span>
                      </v-flex>
                      <v-flex class="text-md-center" md5>
                        <span>{{file.invalidMessage}}</span>
                      </v-flex>
                      <v-flex class="text-md-right" md1>
                        <v-icon small @click="removeFile(index)">fa-times-circle</v-icon>
                      </v-flex>
                    </v-layout>
                  </v-flex>
                  <v-btn class="upload-btn mt-3 mr-2" depressed @click="resetFiles" v-show="this.files.length">reset</v-btn>
              </v-form>
            </div>

          </v-flex>

          <v-flex xs12>
            <v-card-actions>
              <v-layout wrap row>

                <v-flex xs12 md6 class="pl-2">
                  <v-switch label="switch off to hide room from search results" color="success" v-model="room.isReady"></v-switch>
                </v-flex>
                
                <v-flex xs12 md6 class="text-xs-right">
                  <v-btn color="#feae25" large class="elevation-0" :disabled="btnDisabled" @click="submitNewRoom">Add Room</v-btn>
                </v-flex>

              </v-layout>

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
