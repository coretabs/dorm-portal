<template>
<div id="manage-dorm">
  <v-card class="elevation-0">
    <v-card-text class="pa-3">
      <v-form ref="form" lazy-validation>
        <v-layout wrap>
          <v-flex xs12 sm6 md4 pa-3>
            <h2 class="heading">General Properties:</h2>
            <v-select class="shift-left" :items="roomData.room_types" :rules="requiredRules" item-text="name" item-value="id" label="Room Type" append-icon="expand_more" :menu-props="{
            offsetY: '',
            transition: 'slide-y-transition',
            bottom: ''
          }" v-model="roomData.room_type_id"></v-select>

            <v-select class="shift-left" :items="roomData.durations" :rules="requiredRules" item-text="name" item-value="id" label="Duration" append-icon="expand_more" :menu-props="{
            offsetY: '',
            transition: 'slide-y-transition',
            bottom: ''
          }" v-model="roomData.duration_id"></v-select>

            <v-text-field label="Number of people" type="number" :rules="requiredRules" v-model="roomData.people_allowed_number"></v-text-field>

            <v-layout wrap>
              <v-flex xs12 sm8>
                <v-text-field label="price" type="number" :rules="requiredRules" v-model="roomData.price"></v-text-field>
              </v-flex>
              <v-flex xs12 sm4 pl-2>
                <v-select class="shift-left" :rules="requiredRules" :items="roomData.currencies" v-model="roomData.price_currency_id" item-text="code" item-value="id" label="Currency" color="success" append-icon="expand_more" :menu-props="{
                  offsetY: '',
                  transition: 'slide-y-transition',
                  bottom: ''
                }"></v-select>
              </v-flex>
            </v-layout>
            <v-text-field label="Total Rooms in Dorm" hint="Number of all rooms of this type in your dorm" :rules="requiredRules" type="number" v-model="roomData.total_quota"></v-text-field>
            <v-text-field label="Quota" hint="Number of rooms you want to open for online reservation" type="number" :rules="requiredRules" v-model="roomData.allowed_quota"></v-text-field>
            <v-text-field label="Confirmation Duration in Days" hint="Give students a deadline to upload payment receipts" :rules="requiredRules" type="number" v-model="roomData.room_confirmation_days"></v-text-field>

            <v-autocomplete class="features-input" v-model="roomData.chosen_features" :disabled="isUpdating" :items="roomData.all_features" box chips color="blue-grey lighten-2" label="Select features" item-text="name" item-value="id" multiple>
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

            <div v-for="radioFilter in roomData.radio_filters" :key="radioFilter.id">
              <v-select class="shift-left" :items="radioFilter.options" v-model="radioFilter.chosen_option_id" item-text="name" item-value="id" :label="radioFilter.name" append-icon="expand_more" :menu-props="{
                offsetY: '',
                transition: 'slide-y-transition',
                bottom: ''
                }" @change="addFilter(radioFilter.id, radioFilter.chosen_option_id, 'radio')"></v-select>

            </div>

            <div v-for="integralFilter in roomData.integral_filters" :key="integralFilter.id">
              <v-text-field :label="integralFilter.name" v-model="integralFilter.selected_number" @change="addFilter(integralFilter.id, integralFilter.selected_number, 'integral')" type="number"></v-text-field>
            </div>

          </v-flex>

          <v-flex xs12 sm6 md4 pa-3>

            <v-layout row wrap>
              <v-flex xs12>
                <h2 class="heading">Room Photos:</h2>
              </v-flex>
              <template v-if="roomData.photos.length">
                <v-flex class="px-2 pb-3" md3 xs6 v-for="(photo,i) in roomData.photos" :key="i">
                  <v-btn icon class="pa-0" @click="confirmDelete(photo.id)">
                    <v-icon>fa-times</v-icon>
                  </v-btn>
                  <v-img gradient="to top right, rgba(44,40,72,.4), rgba(44,40,72,.4)" :src="photo.url" height="110" width="100%">
                    <v-layout slot="placeholder" fill-height align-center justify-center ma-0>
                      <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
                    </v-layout>
                  </v-img>
                </v-flex>
              </template>
              <template v-else>
                <p class="grey--text">No Photos Has been uploaded for this Room</p>
              </template>
            </v-layout>

            <v-layout column>
              <v-flex xs12 class="mt-4">
                <h2 class="heading">Upload New Photos:</h2>
              </v-flex>
              <v-flex>
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
                      <input type="file" id="file" multiple @change="selectNewFile" ref="files" v-show="false">
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
            </v-layout>
          </v-flex>

          <v-flex xs12>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn large class="elevation-0" @click="closeEditDialog">Cancel</v-btn>

              <v-btn color="#feae25" large class="elevation-0" :disabled="btnDisabled" :loading="loadingBtn" @click="submitChanges">Save Changes</v-btn>
            </v-card-actions>
          </v-flex>

        </v-layout>
      </v-form>
    </v-card-text>
  </v-card>
  <v-dialog v-model="deletePhoto.confirmDialog" width="500" lazy>
    <v-card>
      <v-card-title class="headline text-uppercase font-weight-medium red accent-4 white--text">
        Confirm Delete
      </v-card-title>
      <v-card-text class="subheading my-3">
        Are You sure you want to delete this Photo?
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn class="elevation-0" @click="deletePhoto.confirmDialog = false">Cancel</v-btn>
        <v-btn color="red" class="elevation-0" @click="deleteRoomPhoto" :loading="loadingBtn">Delete photo</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</div>
</template>

<script src="./EditRoom.js"></script>

<style src="./EditRoom.scss" lang="scss"></style>
