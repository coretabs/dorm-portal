<template>
<v-layout row wrap>
  <v-flex xs12 md4 px-3>
    <div id="amount">
      <h3>Amount to pay:</h3>
      <span>$1500</span>
      <v-icon>fa-money-bill-alt</v-icon>
    </div>
    <div id="bank-accounts">
      <h3>Dormitory Bank Accounts:</h3>
      <v-expansion-panel popout>
        <v-expansion-panel-content v-for="(item,i) in 3" :key="i">
          <div slot="header">is Bank</div>
          <v-card>
            <v-card-text>
              bank information
            </v-card-text>
          </v-card>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </div>
  </v-flex>
  <v-flex xs12 md8 px-3>
    <div>
      <v-card class="elevation-0">
        <v-card-text>
          <p>{{lang.confirmPayment.instruction}}</p>
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
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="#feae25" class="elevation-0" @click="e1 = 3" v-if="$refs.upload && $refs.upload.uploaded">{{lang.confirmPayment.confirmButton}}</v-btn>
        </v-card-actions>
      </v-card>
    </div>
  </v-flex>
</v-layout>
</template>

<script src="./ConfirmPayment.js"></script>

<style src="./ConfirmPayment.scss" lang="scss"></style>
