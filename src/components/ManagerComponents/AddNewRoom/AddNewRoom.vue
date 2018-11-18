<template>
<div id="manage-dorm">
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
</div>
</template>

<script src="./AddNewRoom.js"></script>

<style src="./AddNewRoom.scss" lang="scss"></style>
