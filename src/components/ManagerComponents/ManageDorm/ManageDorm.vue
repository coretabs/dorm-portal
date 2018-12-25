<template>
<div id="manage-dorm" class="mt-3 mb-5">
  <v-tabs v-model="active" color="#fff" slider-color="#ffa915">
    <v-tab v-for="n in lang.managerDormInfo.length" :key="n" ripple>
      {{lang.managerDormInfo[n-1]}}
    </v-tab>
    <!-- General Tab -->
    <v-tab-item class="info-tab">
      <v-card>
        <v-card-text class="pa-0">
          <v-layout wrap>

            <v-flex xs12>
              <v-card-actions class="card-header py-3 px-4">
                <h2 class="white--text">{{dorm.name}}</h2>
                <v-spacer></v-spacer>
                <v-btn color="#ffa915" depressed @click="updateDialog('general')">
                  <v-icon small color="black" left>fa-pen</v-icon>
                  Update info
                </v-btn>
              </v-card-actions>
            </v-flex>

            <v-flex xs12 sm6 md8 class="pa-4">

              <v-layout column>
                <h3 class="heading">About Dorm</h3>
                <v-flex>
                  <v-tabs color="#fafafa" slider-color="#feae25">

                    <v-tab v-for="(language,index) in languages" :key="index" ripple>
                      {{language.code}}
                    </v-tab>

                    <v-tab-item class="pa-3" v-for="(about,index) in dorm.abouts" :key="index">
                      <p class="about">{{about}}</p>
                    </v-tab-item>

                  </v-tabs>
                </v-flex>
              </v-layout>

            </v-flex>

            <v-flex xs12 sm6 md4 pa-3 class=" pa-4 pl-0">
              <v-layout column class="mb-4">
                <h3 class="mb-1">
                  Manager Name
                </h3>
                <span small class="title font-weight-regular ">
                  {{dorm.contact_name}}
                </span>
              </v-layout>

              <v-layout column class="mb-4">
                <h3 class="mb-1">
                  Email
                </h3>
                <span class="title font-weight-regular ">
                  {{dorm.contact_email}}
                </span>
              </v-layout>

              <v-layout column class="mb-4">
                <h3 class="mb-1">
                  Phone Number
                </h3>
                <span class="title font-weight-regular ">
                  {{dorm.contact_number}}
                </span>
              </v-layout>

              <v-layout column class="mb-4">
                <h3 class="mb-1">
                  Fax Number
                </h3>
                <span class="title font-weight-regular ">
                  {{dorm.contact_fax}}
                </span>
              </v-layout>

            </v-flex>

          </v-layout>

        </v-card-text>
      </v-card>

      <v-dialog persistent v-if="dorm" v-model="dialog.general" width="1200">
        <v-card>
          <v-form ref="form" lazy-validation>
            <v-card-text>
              <v-layout row wrap>

                <v-flex sm12 md8 pa-3>
                  <h3 class="heading mb-4">About {{dorm.name}}:</h3>
                  <div>
                    <v-tabs color="#fafafa" slider-color="#feae25">

                      <v-tab v-for="(language,index) in languages" :key="index" ripple>
                        {{language.code}}
                      </v-tab>

                      <v-tab-item v-for="(about,index) in dorm.abouts" :key="index">
                        <v-textarea rows="9" v-model="dorm.abouts[index]" :placeholder="lang.DormGeneralinfo.DormDescription" :rules="requiredRules" required></v-textarea>
                      </v-tab-item>

                    </v-tabs>
                  </div>
                </v-flex>

                <v-flex sm12 md4 pa-3>
                  <h3 class="heading mb-3">Contact Information:</h3>
                  <v-text-field v-model="dorm.contact_name" prepend-icon="fa-user" :label="lang.DormGeneralinfo.DormPhone" type="text" :rules="requiredRules" required></v-text-field>
                  <v-text-field v-model="dorm.contact_number" prepend-icon="fa-mobile-alt" :label="lang.DormGeneralinfo.DormPhone" type="text" :rules="requiredRules" required></v-text-field>
                  <v-text-field v-model="dorm.contact_fax" prepend-icon="fa-fax" :label="lang.DormGeneralinfo.DormFax" type="text" :rules="requiredRules" required></v-text-field>
                  <v-text-field v-model="dorm.contact_email" prepend-icon="fa-envelope" :label="lang.DormGeneralinfo.DormEmail" type="text" :rules="requiredRules" required></v-text-field>
                </v-flex>

                <v-flex xs12>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn class="elevation-0" @click="closeDialog('general')">Cancel</v-btn>
                    <v-btn color="#feae25" class="elevation-0" @click="submitDormInfo">{{lang.DormGeneralinfo.button}}</v-btn>
                  </v-card-actions>
                </v-flex>

              </v-layout>

            </v-card-text>
          </v-form>
        </v-card>
      </v-dialog>
    </v-tab-item>

    <!-- Location Tab -->
    <v-tab-item class="location-tab">
      <v-card>
        <v-card-text class="pa-0">
          <v-layout wrap>

            <v-flex xs12>
              <v-card-actions class="card-header py-3 px-4">
                <h2 class="white--text">Dorm Location</h2>
                <v-spacer></v-spacer>
                <v-btn color="#ffa915" depressed >
                  <v-icon small color="black" left>fa-pen</v-icon>
                  Update Address
                </v-btn>
              </v-card-actions>
            </v-flex>

            <v-flex xs12 md12 pa-3>
              <v-layout row wrap>

                <v-flex xs12 pa-3>
                  <h3 class="heading">
                    <v-icon small class="pr-2">fa-map-marker-alt</v-icon>
                    Address
                  </h3>
                  <span class="title font-weight-regular">
                    Next to Computer Department
                  </span>
                </v-flex>

                <v-flex xs12 pa-3>
                  <h3 class="heading">
                    <v-icon small class="pr-2">fa-map-pin</v-icon>
                    Latitude
                  </h3>
                  <span class="title font-weight-regular">
                    31.2255558
                  </span>
                </v-flex>

                <v-flex xs12 pa-3>
                  <h3 class="heading">
                    <v-icon class="pr-2">fa-map-pin</v-icon>
                    Longitude
                  </h3>
                  <span class="title font-weight-regular">
                    31.2255558
                  </span>
                </v-flex>

              </v-layout>

            </v-flex>

            <!-- <v-flex xs12 md6 pa-3>
              <v-text-field prepend-icon="fa-map-marker-alt" :label="lang.DormGeneralinfo.DormAddress" type="text"></v-text-field>
              <v-layout>
                <v-flex xs12 sm6 pr-1>
                  <v-text-field prepend-icon="fa-map-pin" :label="lang.DormGeneralinfo.DormLatitude" type="text"></v-text-field>
                </v-flex>
                <v-flex xs12 sm6 pl-1>
                  <v-text-field prepend-icon="fa-map-pin" :label="lang.DormGeneralinfo.DormLongitude" type="text"></v-text-field>
                </v-flex>
              </v-layout>
            </v-flex> -->

            <v-flex xs12 md6 pa-3>

            </v-flex>

          </v-layout>
        </v-card-text>
      </v-card>
    </v-tab-item>

    <!-- Features Tab -->
    <v-tab-item class="Features-tab">
      <v-card>
        <v-card-text class="pa-0">
          <v-layout wrap>

            <v-flex xs12>
              <v-card-actions class="card-header py-3 px-4">
                <h2 class="white--text">Dorm Features</h2>
                <v-spacer></v-spacer>
                <v-btn color="#ffa915" depressed >
                  <v-icon small color="black" left>fa-pen</v-icon>
                  Update Features
                </v-btn>
              </v-card-actions>
            </v-flex>

            <!-- <v-flex xs12 md12 pa-3>

              <v-autocomplete v-model="selectedFeatures" :disabled="isUpdating" :items="Features" box chips color="blue-grey lighten-2" label="Select" item-text="name" item-value="id" multiple>
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

            </v-flex> -->

          </v-layout>
        </v-card-text>
      </v-card>
    </v-tab-item>

    <!-- Photos Tab -->
    <v-tab-item class="photos-tab">
      <v-card>
        <v-card-text class="pa-0">
          <v-layout wrap>

            <v-flex xs12>
              <v-card-actions class="card-header py-3 px-4">
                <h2 class="white--text">Dorm Photos</h2>
                <v-spacer></v-spacer>
                <v-btn color="#ffa915" depressed >
                  <v-icon small color="black" left>fa-pen</v-icon>
                  Update Features
                </v-btn>
              </v-card-actions>
            </v-flex>

            <v-flex xs12 md6 pa-3>
              das
            </v-flex>

            <!-- <v-flex xs12 md6 pa-3>
              <h3 class="heading">Dorm Photos:</h3>
              <div class="drag-drop">
                <div class="upload">
                  <ul v-if="files.length">
                    <li v-for="file in files" :key="file.id">
                      <span>{{file.name}}</span> -
                      <span>{{file.size | formatSize}}</span> -
                      <span v-if="file.error">{{file.error}}</span>
                      <span v-else-if="file.success">success</span>
                      <span v-else-if="file.active">active</span>
                      <span v-else-if="file.active">active</span>
                      <span v-else></span>
                    </li>
                  </ul>
                  <ul v-else>
                    <div>
                      <v-icon>fa-file-import</v-icon>
                      <h4>{{lang.confirmPayment.dragMessage}}</h4>
                      <label for="file">{{lang.confirmPayment.chooseFile}}</label>
                    </div>
                  </ul>

                  <div v-show="$refs.upload && $refs.upload.dropActive" class="drop-active">
                    <h3>{{lang.confirmPayment.dragMessage}}</h3>
                  </div>
                </div>

                <v-flex class="action-btn">
                  <file-upload class="select-btn" post-action="/upload/post" :multiple="true" :drop="true" :drop-directory="true" v-model="files" ref="upload">
                    <v-icon color="#5472a6" small>fa-plus</v-icon>
                    {{lang.confirmPayment.selectFile}}
                  </file-upload>

                  <v-btn color="#58b44e" dark class="elevation-0" v-if="!$refs.upload || !$refs.upload.active" @click.prevent="$refs.upload.active = true">
                    <v-icon color="#0e7426" left small>fa-arrow-up</v-icon>
                    {{lang.confirmPayment.startUpload}}
                  </v-btn>

                  <v-btn color="red darken-1" dark class="elevation-0" v-else @click.prevent="$refs.upload.active = false">
                    <v-icon left>fa-times-circle</v-icon>
                    {{lang.confirmPayment.stopUpload}}
                  </v-btn>

                </v-flex>
              </div>

            </v-flex> -->

          </v-layout>
        </v-card-text>
      </v-card>
    </v-tab-item>

    <!-- Bank Account Tab -->
    <v-tab-item class="photos-tab">
      <v-card>
        <v-card-text class="pa-0">
          <v-layout wrap>

            <v-flex xs12>
              <v-card-actions class="card-header py-3 px-4">
                <h2 class="white--text">Bank Accounts</h2>
                <v-spacer></v-spacer>
                <v-btn color="#ffa915" depressed >
                  <v-icon small color="black" left>fa-pen</v-icon>
                  Update Features
                </v-btn>
              </v-card-actions>
            </v-flex>

            <v-flex xs12 md6 pa-3>
              das
            </v-flex>

          </v-layout>
        </v-card-text>
      </v-card>
    </v-tab-item>

  </v-tabs>

</div>
</template>

<script src="./ManageDorm.js"></script>

<style src="./ManageDorm.scss" lang="scss"></style>
