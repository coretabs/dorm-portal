<template>
<div id="manage-dorm">
  <v-tabs v-model="active" color="#fdfdfd" slider-color="#999">
    <v-tab v-for="n in lang.managerDormInfo.length" :key="n" ripple>
      {{lang.managerDormInfo[n-1]}}
    </v-tab>
    <!-- General Tab -->
    <v-tab-item class="info-tab">
      <v-card>
        <v-card-text>
          <v-layout wrap>

            <v-flex xs12 sm6 md8 pa-3>
              <h3 class="heading">General Information:</h3>
              <v-text-field v-model="dormName" :label="lang.DormGeneralinfo.DormName" type="text" disabled></v-text-field>
              <div>
                <v-tabs color="#fafafa" slider-color="#feae25">

                  <v-tab v-for="(language,index) in languages" :key="index" ripple>
                    {{language.code}}
                  </v-tab>

                  <v-tab-item v-for="(language,index) in languages" :key="index">
                    <v-textarea v-model="desc" :placeholder="lang.DormGeneralinfo.DormDescription"></v-textarea>
                  </v-tab-item>

                </v-tabs>
              </div>
            </v-flex>

            <v-flex xs12 sm6 md4 pa-3>
              <h3 class="heading">Contact Information:</h3>
              <v-text-field prepend-icon="fa-phone" :label="lang.DormGeneralinfo.DormPhone" type="text"></v-text-field>
              <v-text-field prepend-icon="fa-mobile-alt" :label="lang.DormGeneralinfo.DormMobile" type="text"></v-text-field>
              <v-text-field prepend-icon="fa-fax" :label="lang.DormGeneralinfo.DormFax" type="text"></v-text-field>
              <v-text-field prepend-icon="fa-envelope" :label="lang.DormGeneralinfo.DormEmail" type="text"></v-text-field>
            </v-flex>

            <v-flex xs12>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="#feae25" large class="elevation-0" @click="submit">{{lang.DormGeneralinfo.button}}</v-btn>
              </v-card-actions>
            </v-flex>

          </v-layout>

        </v-card-text>
      </v-card>
    </v-tab-item>

    <!-- Location Tab -->
    <v-tab-item class="location-tab">
      <v-card>
        <v-card-text>
          <v-layout wrap>

            <v-flex xs12 md6 pa-3>
              <h3 class="heading">Dorm Location:</h3>
              <v-text-field prepend-icon="fa-map-marker-alt" :label="lang.DormGeneralinfo.DormAddress" type="text"></v-text-field>
              <v-layout>
                <v-flex xs12 sm6 pr-1>
                  <v-text-field prepend-icon="fa-map-pin" :label="lang.DormGeneralinfo.DormLatitude" type="text"></v-text-field>
                </v-flex>
                <v-flex xs12 sm6 pl-1>
                  <v-text-field prepend-icon="fa-map-pin" :label="lang.DormGeneralinfo.DormLongitude" type="text"></v-text-field>
                </v-flex>
              </v-layout>
            </v-flex>

            <v-flex xs12 md6 pa-3>

            </v-flex>

            <v-flex xs12>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="#feae25" large class="elevation-0" @click="submit">{{lang.DormGeneralinfo.button}}</v-btn>
              </v-card-actions>
            </v-flex>

          </v-layout>
        </v-card-text>
      </v-card>
    </v-tab-item>

    <!-- Features Tab -->
    <v-tab-item class="Features-tab">
      <v-card>
        <v-card-text>
          <v-layout wrap>

            <v-flex xs12 md12 pa-3>
              <h3 class="heading">Dorm Features:</h3>

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

            </v-flex>

            <v-flex xs12 md6 pa-3>

            </v-flex>

            <v-flex xs12>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="#feae25" large class="elevation-0" @click="submit">{{lang.DormGeneralinfo.button}}</v-btn>
              </v-card-actions>
            </v-flex>

          </v-layout>
        </v-card-text>
      </v-card>
    </v-tab-item>

    <!-- Photos Tab -->
    <v-tab-item class="photos-tab">
      <v-card>
        <v-card-text>
          <v-layout wrap>

            <v-flex xs12 md6 pa-3>
              <h3 class="heading">Cover Photo:</h3>

            </v-flex>

            <v-flex xs12 md6 pa-3>
              <h3 class="heading">Dorm Photo:</h3>
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
                    <v-icon left>fa-plus</v-icon>
                    {{lang.confirmPayment.selectFile}}
                  </file-upload>

                  <v-btn color="#1c3a70" dark class="elevation-0" v-if="!$refs.upload || !$refs.upload.active" @click.prevent="$refs.upload.active = true">
                    <v-icon left>fa-arrow-up</v-icon>
                    {{lang.confirmPayment.startUpload}}
                  </v-btn>

                  <v-btn color="red darken-1" dark class="elevation-0" v-else @click.prevent="$refs.upload.active = false">
                    <v-icon left>fa-times-circle</v-icon>
                    {{lang.confirmPayment.stopUpload}}
                  </v-btn>

                </v-flex>
              </div>

            </v-flex>

            <v-flex xs12>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="#feae25" large class="elevation-0" @click="submit">{{lang.DormGeneralinfo.button}}</v-btn>
              </v-card-actions>
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
