<template>
<div id="manage-dorm" class="mt-2 mb-5">
  <v-tabs v-model="active" color="#fff" slider-color="#ffa915">
    <v-tab v-for="n in lang.managerDormInfo.length" :key="n" ripple>
      {{lang.managerDormInfo[n-1]}}
    </v-tab>
    <!-- General Tab -->
    <v-tab-item class="info-tab" lazy>
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
      <v-dialog persistent v-if="dorm" v-model="dialog.general" width="1200" lazy>
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
                  <v-text-field v-model="dorm.contact_email" prepend-icon="fa-envelope" :label="lang.DormGeneralinfo.DormEmail" type="text" :rules="emailRules" required></v-text-field>
                  <v-text-field v-model="dorm.contact_number" prepend-icon="fa-mobile-alt" :label="lang.DormGeneralinfo.DormPhone" type="text" :rules="requiredRules" required></v-text-field>
                  <v-text-field v-model="dorm.contact_fax" prepend-icon="fa-fax" :label="lang.DormGeneralinfo.DormFax" type="text" :rules="requiredRules" required></v-text-field>

                </v-flex>
                <v-flex xs12>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn class="elevation-0" @click="closeDialog('general')">Cancel</v-btn>
                    <v-btn color="#feae25" class="elevation-0" @click="submitDormInfo('general')" :loading="loadingBtn">{{lang.DormGeneralinfo.button}}</v-btn>
                  </v-card-actions>
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-form>
        </v-card>
      </v-dialog>
    </v-tab-item>

    <!-- Location Tab -->
    <v-tab-item class="location-tab" lazy>
      <v-card>
        <v-card-text class="pa-0">
          <v-layout wrap row>
            <v-flex xs12>
              <v-card-actions class="card-header py-3 px-4">
                <h2 class="white--text">Dorm Location</h2>
                <v-spacer></v-spacer>
                <v-btn color="#ffa915" depressed @click="updateDialog('location')">
                  <v-icon small color="black" left>fa-pen</v-icon>
                  Update Address
                </v-btn>
              </v-card-actions>
            </v-flex>
            <v-flex xs12 md4 pa-3>
              <v-layout row wrap>
                <v-flex xs12 pa-3>
                  <h3 class="heading">
                    <v-icon small class="pr-2">fa-map-marker-alt</v-icon>
                    Address
                  </h3>
                  <span class="title font-weight-regular">
                    {{dorm.address}}
                  </span>
                </v-flex>
                <v-flex xs12 pa-3>
                  <h3 class="heading">
                    <v-icon small class="pr-2">fa-map-pin</v-icon>
                    Latitude
                  </h3>
                  <span class="title font-weight-regular">
                    {{dorm.geo_latitude}}
                  </span>
                </v-flex>
                <v-flex xs12 pa-3>
                  <h3 class="heading">
                    <v-icon class="pr-2">fa-map-pin</v-icon>
                    Longitude
                  </h3>
                  <span class="title font-weight-regular">
                    {{dorm.geo_longitude}}
                  </span>
                </v-flex>
              </v-layout>
            </v-flex>

            <v-flex xs12 md8 pa-3>
              <dorm-map ref=map v-show="!dialog.location" style="z-index: 0" :longitude="dorm.geo_longitude" :latitude="dorm.geo_latitude"></dorm-map>
            </v-flex>

            <v-dialog persistent v-if="dorm" v-model="dialog.location" width="800" lazy>
              <v-card>
                <v-form ref="form" lazy-validation>
                  <v-card-text>
                    <v-layout row wrap>
                      <v-flex xs12 pa-3>
                        <h2 class="mb-4">Update Dorm Address</h2>
                        <v-text-field v-model="dorm.address" prepend-icon="fa-map-marker-alt" :label="lang.DormGeneralinfo.DormAddress" type="text"></v-text-field>
                        <v-layout wrap row>
                          <v-flex xs12 sm6 pr-1>
                            <v-text-field prepend-icon="fa-map-pin" v-model="dorm.geo_latitude" :label="lang.DormGeneralinfo.DormLatitude" type="text"></v-text-field>
                          </v-flex>
                          <v-flex xs12 sm6 pl-1>
                            <v-text-field prepend-icon="fa-map-pin" v-model="dorm.geo_longitude" :label="lang.DormGeneralinfo.DormLongitude" type="text"></v-text-field>
                          </v-flex>
                          <v-flex class="mt-4 text-sm-center" xs12>
                            <p>You can get your dorm Latitude and Longitude from <a href="https://www.latlong.net" target="_blank">here</a> or just click on the following button</p>
                            <v-btn color="success" @click="getGeolocation">Get my Location</v-btn>
                          </v-flex>
                        </v-layout>
                      </v-flex>
                      <v-flex xs12>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn class="elevation-0" @click="closeDialog('location')">Cancel</v-btn>
                          <v-btn color="#feae25" class="elevation-0" @click="submitDormLocation('location')" :loading="loadingBtn">{{lang.DormGeneralinfo.button}}</v-btn>
                        </v-card-actions>
                      </v-flex>
                    </v-layout>
                  </v-card-text>
                </v-form>
              </v-card>
            </v-dialog>

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
                <v-btn color="#ffa915" depressed @click="updateDialog('features')">
                  <v-icon small color="black" left>fa-pen</v-icon>
                  Update Features
                </v-btn>
              </v-card-actions>
            </v-flex>

            <v-flex xs12 class="pa-3">
              <div class="dorm-feature" v-for="feature in dorm.features" :key="feature.id">
                <v-icon v-if="feature.icon">{{feature.icon}}</v-icon>
                <v-icon else>fa-check</v-icon>
                <span>{{feature.name}}</span>
              </div>
            </v-flex>

            <v-dialog persistent v-if="dorm" v-model="dialog.features" width="800" lazy>
              <v-card>
                <v-form ref="form" lazy-validation @submit.prevent>
                  <v-card-text class="pb-4">
                    <v-layout row wrap>
                      <v-flex xs12 class="mb-4">
                        <v-card-actions>
                          <h2>Update Dorm Features</h2>
                          <v-spacer></v-spacer>
                          <v-btn class="elevation-0" @click="closeDialog('features')">Cancel</v-btn>
                          <v-btn color="#feae25" class="elevation-0" @click="submitDormFeatures('features')" :loading="loadingBtn">{{lang.DormGeneralinfo.button}}</v-btn>
                        </v-card-actions>
                      </v-flex>
                      <v-flex xs12 md12 class="pa-3">
                        <v-autocomplete v-model="selectedFeatures" :disabled="isUpdating" :items="dorm.all_features" box chips color="blue-grey lighten-2" label="Select" item-text="name" item-value="id" multiple>
                          <template slot="selection" slot-scope="data">
                            <v-chip :selected="data.selected" close dark class="chip--select-multi" @input="remove(data.item)">
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
                    </v-layout>
                  </v-card-text>
                </v-form>
              </v-card>
            </v-dialog>
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
                <!-- <v-spacer></v-spacer>
                <v-btn color="#ffa915" depressed @click="updateDialog('features')">
                  <v-icon small color="black" left>fa-pen</v-icon>
                  Add Photo
                </v-btn> -->
              </v-card-actions>
            </v-flex>

            <v-flex xs12 md6 class="pa-4">
              <v-layout row wrap>
                <v-flex>
                  <h3 class="mb-4">Cover Photo {{dorm.id}}</h3>
                  <v-card>
                    <label class="update-cover__btn" for="cover-img">
                      <v-icon small>fa-pen</v-icon>
                      Update Cover
                    </label>
                    <v-img v-if="dorm.cover" gradient="to top right, rgba(44,40,72,.4), rgba(44,40,72,.4)" :src="dorm.cover" height="350" width="100%">
                      <v-layout slot="placeholder" fill-height align-center justify-center ma-0>
                        <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
                      </v-layout>
                    </v-img>
                    <v-layout v-else class="cover-block" align-center justify-center row>
                      <v-icon>fa-image</v-icon>
                    </v-layout>
                    <input type="file" id="cover-img" @change="selectCover" ref="coverFile" v-show="false"></input>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-flex>

            <v-flex xs12 md6 class="pa-4">
              <v-layout row wrap>
                <v-flex>
                  <v-layout class="mb-4">
                    <h3 class="ma-0 pa-0">Dorm Photos</h3>
                    <v-spacer></v-spacer>
                    <!-- <v-btn color="#ffa915" depressed @click="updateDialog('features')">
                      <v-icon small color="black" left>fa-pen</v-icon>
                      Add Photo
                    </v-btn> -->
                  </v-layout>
                  <v-layout v-if="dorm.photos.length">
                    asd
                  </v-layout>

                  <v-layout v-else class="photos-block" align-center justify-center row>
                    <p>You haven't uploaded any photos yet.</p>
                  </v-layout>
                </v-flex>
              </v-layout>
            </v-flex>

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
                <v-btn color="#ffa915" depressed @click="updateDialog('addBanks')">
                  <v-icon small color="black" left>fa-pen</v-icon>
                  Add new account
                </v-btn>
              </v-card-actions>
            </v-flex>

            <v-flex xs12>
              <v-card class="elevation-0">
                <v-card-title>
                  <v-flex xs12 md3>
                    <v-text-field v-model="search" prepend-icon="search" @input="filterByStatus()" label="Search" single-line hide-details></v-text-field>
                  </v-flex>
                </v-card-title>

                <v-data-table :must-sort="bankAccounts.id" :headers="headers" :items="bankAccounts" :search="search" :rows-per-page-items="rowsPerPage" :pagination.sync="pagination">
                  <template slot="items" slot-scope="props">
                    <td class="text-xs-left">{{props.item.id}}</td>
                    <td class="text-xs-left">{{props.item.bank_name}}</td>
                    <td class="text-xs-left">{{props.item.account_name}}</td>
                    <td class="text-xs-left">{{props.item.account_number}}</td>
                    <td class="text-xs-left">{{props.item.swift}}</td>
                    <td class="text-xs-left">{{props.item.iban}}</td>
                    <td class="text-xs-left">{{props.item.currency_code}}</td>
                    <td class="text-xs-left layout pl-3">
                      <v-tooltip top>
                        <v-btn slot="activator" @click="updateDialog('addBanks', true, props.item)" flat icon>
                          <v-icon small color="#677889">fa-pen</v-icon>
                        </v-btn>
                        <span>Edit</span>
                      </v-tooltip>
                      <v-tooltip top>
                        <v-btn slot="activator" @click="confirmDelete(props.item.id)" flat icon>
                          <v-icon small color="#677889">fa-trash</v-icon>
                        </v-btn>
                        <span>Delete</span>
                      </v-tooltip>

                    </td>
                  </template>
                  <v-alert slot="no-results" :value="true" color="error" icon="warning">
                    {{lang.manageResrevations.searchResults}} "{{ search }}".
                  </v-alert>
                </v-data-table>
              </v-card>

              <v-dialog v-model="deleteRecord.confirmDialog" width="500" lazy>
                <v-card>
                  <v-card-title class="headline text-uppercase font-weight-medium red accent-4 white--text">
                    Confirm Delete
                  </v-card-title>
                  <v-card-text class="subheading my-3">
                    Are You sure you want to delete this bank account?
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn class="elevation-0" @click="deleteRecord.confirmDialog = false">Cancel</v-btn>
                    <v-btn color="red" class="elevation-0" @click="deleteBankAccount" :loading="loadingBtn">Delete</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>

            </v-flex>

            <v-dialog persistent v-if="dorm" v-model="dialog.addBanks" width="600" lazy>
              <v-card>
                <v-form ref="form" lazy-validation>
                  <v-card-text>
                    <v-layout row wrap>
                      <v-flex xs12 md12 class="pa-3">
                        <h2 class="mb-4">Add new Bank Account</h2>
                        <v-text-field v-model="bank.name" label="Bank Name" type="text" :rules="requiredRules" required></v-text-field>
                        <v-text-field v-model="bank.accountName" label="Account Name" type="text" :rules="requiredRules" required></v-text-field>
                        <v-select class="shift-left" v-model="bank.currency" :items="currencies" item-text="code" item-value="code" label="Currency" color="success" append-icon="expand_more" :menu-props="{
                          offsetY: '',
                          transition: 'slide-y-transition',
                          bottom: ''
                        }" :rules="requiredRules" required></v-select>
                        <v-text-field v-model="bank.accountNumber" label="Account Number" type="text" :rules="requiredRules" required></v-text-field>
                        <v-text-field v-model="bank.iban" label="IBAN" type="text" :rules="requiredRules" required></v-text-field>
                        <v-text-field v-model="bank.swift" label="Swift" type="text"></v-text-field>
                      </v-flex>
                      <v-flex xs12>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn class="elevation-0" @click="closeDialog('addBanks')">Cancel</v-btn>
                          <v-btn v-if="!dialog.isEdit" color="#feae25" class="elevation-0" @click="submitNewBank" :loading="loadingBtn">Add Bank</v-btn>
                          <v-btn v-if="dialog.isEdit" color="#feae25" class="elevation-0" @click="updateBankAccount" :loading="loadingBtn">Update</v-btn>
                        </v-card-actions>
                      </v-flex>
                    </v-layout>
                  </v-card-text>
                </v-form>
              </v-card>
            </v-dialog>

          </v-layout>
        </v-card-text>
      </v-card>
    </v-tab-item>

  </v-tabs>

</div>
</template>

<script src="./ManageDorm.js"></script>

<style src="./ManageDorm.scss" lang="scss"></style>
