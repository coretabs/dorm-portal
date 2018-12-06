<template>
<div id="manage-dorm">
  <v-card>
    <v-card-text>
      <v-layout wrap>

        <v-flex xs12 sm6 md4 pa-3>
          <h3 class="heading">General Spec:</h3>

          <v-select class="shift-left" :items="rooms_data.room_types" item-text="name" item-value="id" label="Room Type" solo color="success" append-icon="expand_more" :menu-props="{
            offsetY: '',
            transition: 'slide-y-transition',
            bottom: ''
          }"></v-select>

          
          <v-select class="shift-left" :items="rooms_data.durations" item-text="name" item-value="id" label="Duration" solo color="success" append-icon="expand_more" :menu-props="{
            offsetY: '',
            transition: 'slide-y-transition',
            bottom: ''
          }"></v-select>

          <v-text-field label="Number of people" type="number"></v-text-field>

          <v-layout wrap>
            <v-flex xs12 sm8>
              <v-text-field label="price" type="number"></v-text-field>
            </v-flex>
            <v-flex xs12 sm4 pl-2>
              <v-select class="shift-left" :items="rooms_data.currencies" item-text="code" item-value="id" label="Currency" solo color="success" append-icon="expand_more" :menu-props="{
            offsetY: '',
            transition: 'slide-y-transition',
            bottom: ''
          }"></v-select>
            </v-flex>
          </v-layout>

          <v-text-field label="Total Rooms in Dorm" type="number"></v-text-field>
          <v-text-field label="Confirmation Duration in Days" type="number"></v-text-field>
        </v-flex>

        <v-flex xs12 sm6 md4 pa-3>
          <h3 class="heading">Room Features:</h3>

          <v-autocomplete v-model="selectedFeatures" :disabled="isUpdating" :items="rooms_data.room_features" box chips color="blue-grey lighten-2" label="Select features" item-text="name" item-value="id" multiple>
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

          <div v-for="(feature,i) in rooms_data.radio_filters" :key="i">
            <v-select class="shift-left" :items="feature.choices" item-text="name" item-value="id" :label="feature.name" solo color="success" append-icon="expand_more" :menu-props="{
            offsetY: '',
            transition: 'slide-y-transition',
            bottom: ''
          }"></v-select>
          </div>


          <div v-for="(feature,i) in rooms_data.integral_filters" :key="i">
            <v-text-field :label="feature.name" type="number"></v-text-field>
          </div>

        </v-flex>


        <v-flex xs12 sm6 md4 pa-3>
          <h3 class="heading">Room Photos:</h3>

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
                    <v-icon color="#5472a6"  small>fa-plus</v-icon>
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

        </v-flex>


        <v-flex xs12>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="#feae25" large class="elevation-0" @click="submit">Add Room</v-btn>
          </v-card-actions>
        </v-flex>

      </v-layout>

    </v-card-text>
  </v-card>
</div>
</template>

<script src="./AddNewRoom.js"></script>

<style src="./AddNewRoom.scss" lang="scss"></style>
