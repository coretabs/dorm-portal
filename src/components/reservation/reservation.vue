<template>
   <v-content id="reservation">
      <v-container fluid fill-height>
        <v-layout justify-center>
          <v-flex xs12 sm8 md6>
          <v-stepper v-model="e1">
            <v-stepper-header class="elevation-3">
              <v-stepper-step :complete="e1 > 1" step="1" color="#1c3a70">Signup</v-stepper-step>

              <v-divider></v-divider>

              <v-stepper-step :complete="e1 > 2" step="2" color="#1c3a70">Confirm Payment</v-stepper-step>

              <v-divider></v-divider>

              <v-stepper-step step="3" color="#1c3a70">Await Approval</v-stepper-step>
            </v-stepper-header>

            <v-stepper-items>
              <v-stepper-content step="1">
                <v-card class="elevation-0">
                  <v-card-text>
                    <v-form>
                      <v-text-field 
                      :label="lang.signup.firstName" 
                      type="text"></v-text-field>
                      <v-text-field 
                      :label="lang.signup.lastName" 
                      type="text"></v-text-field>
                      <v-text-field 
                      :label="lang.signup.passport" 
                      type="text"></v-text-field>
                      <v-text-field 
                      :label="lang.signup.email" 
                      type="email"></v-text-field>
                      <v-text-field 
                      :label="lang.signup.password" 
                      :append-icon="show ? 'visibility_off' : 'visibility'"
                      @click:append="show = !show"
                      :type="show ? 'text' : 'password'"
                      ></v-text-field>
                    </v-form>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="#feae25" large class="elevation-0" @click="e1 = 2">{{lang.signup.button}}</v-btn>
                  </v-card-actions>
                </v-card>
              </v-stepper-content>

              <v-stepper-content step="2">
              
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
                            <v-expansion-panel-content
                              v-for="(item,i) in 3"
                              :key="i"
                            >
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
                                    <file-upload
                                      class="select-btn"
                                      post-action="/upload/post"
                                      :multiple="true"
                                      :drop="true"
                                      :drop-directory="true"
                                      v-model="files"
                                      ref="upload">
                                      <v-icon left>fa-plus</v-icon>
                                      {{lang.confirmPayment.selectFile}}
                                    </file-upload>

                                    <v-btn color="#1c3a70" dark class="elevation-0" v-if="!$refs.upload || !$refs.upload.active"  @click.prevent="$refs.upload.active = true">
                                      <v-icon left>fa-arrow-up</v-icon>
                                      {{lang.confirmPayment.startUpload}}
                                    </v-btn>

                                    <v-btn color="red darken-1" dark class="elevation-0" v-else  @click.prevent="$refs.upload.active = false">
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
                  
              </v-stepper-content>

              <v-stepper-content step="3">
                
                <v-layout id="status-step" row wrap>
                      <v-flex xs12 md4>
                        
                      <div class="uploaded-file">
                        <v-list two-line subheader>
                          <v-subheader inset>Uploaded Documents </v-subheader>
                          <v-list-tile v-for="item in items" :key="item.title" avatar @click="">
                            <v-list-tile-content>
                              <v-list-tile-title>{{ item.title }}</v-list-tile-title>
                              <v-list-tile-sub-title>{{ item.subtitle }}</v-list-tile-sub-title>
                            </v-list-tile-content>
                            <v-list-tile-action>
                              <v-btn icon>
                                <v-icon color="grey lighten-1">fa-eye</v-icon>
                              </v-btn>
                            </v-list-tile-action>
                          </v-list-tile>
                        </v-list>
                        <v-btn color="#feae25" class="elevation-0" @click="e1 = 2" v-if="$refs.upload && $refs.upload.uploaded">{{lang.confirmPayment.confirmButton}}</v-btn>
                        </div>
                         
                      </v-flex>

                      <v-flex xs12 md8>
                        <div class="status-row">
                          <h3>Reservation Status:</h3>
                          <span><v-icon>fa-spinner</v-icon> Pending</span>
                        </div>
                         <div class="status-row">
                          <h3>Comment:</h3>
                          <span>Your payment is being reviewed.</span>
                        </div>
                        <div class="status-row">
                          <h3>Submitted on:</h3>
                          <span>17/08/2018</span>
                        </div>
                      </v-flex>
                      
                    </v-layout>
                
              </v-stepper-content>
            </v-stepper-items>
          </v-stepper>
          </v-flex>

        </v-layout>
      </v-container>
    </v-content>
</template>

<script>
import FileUpload from "vue-upload-component/src";
export default {
  name: "Reservation",
  data: function() {
    return {
      e1: 0,
      show: false,
      password: "Password",
      files: [],
      items: [
          {iconClass: 'grey lighten-1 white--text', title: 'Receipt01', subtitle: 'Jan 9, 2014' },
          {iconClass: 'grey lighten-1 white--text', title: 'Receipt02', subtitle: 'Jan 17, 2014' },
          {iconClass: 'grey lighten-1 white--text', title: 'Receipt03', subtitle: 'Jan 28, 2014' }
        ]
    };
  },
  components: {
    "file-upload": FileUpload
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  }
};
</script>

<style lang="scss">
@import "../../assets/styles/vars";
@import "../../assets/styles/mixins";
@import "~vue-upload-component/dist/vue-upload-component.part.css";
#reservation {
  .container {
    background: $gray-background;
  }
  .layout {
    margin-top: 30px;
    .v-stepper {
      @include radius(4px);
    }
    .v-card {
      @include radius(4px);
      .v-btn {
        @include radius(4px);
      }
      .v-icon {
        font-size: 20px;
      }
    }
  }
  #amount {
    background: $light-green-color;
    padding: 20px;
    @include radius(4px);
    position: relative;
    h3 {
      color: $white-color;
      font-weight: 400;
    }
    span {
      font-size: 32px;
      font-weight: 600;
    }
    .v-icon {
      position: absolute;
      right: 50px;
      top: 0;
      bottom: 0;
      font-size: 42px;
      color: rgba(0, 0, 0, 0.3);
    }
  }
  #bank-accounts {
    margin: 40px 0;
    h3 {
      color: $gray-color;
      margin-bottom: 20px;
    }
    .v-expansion-panel__container {
      @include radius(4px);
    }
  }
  .drag-drop{
    .upload{
      padding: 40px 20px;
      @include radius(4px);
      border: 2px dashed $light-gray-color;
      text-align: center;
      margin: 20px 0;
      .v-icon{
        font-size: 60px;
        color: $light-gray-color;
        margin-bottom: 20px;
      }
      label{
        margin-top: 5px;
        text-decoration: underline;
        cursor: pointer;
      }
      ul {
        list-style: none;
        margin: 0;
        padding: 0;
        li{
          padding: 5px 0;
          margin: 4px 0;
          background: $gray-background;
        }
      }
    }
    .drop-active {
      top: 0;
      bottom: 0;
      right: 0;
      left: 0;
      position: fixed;
      z-index: 9999;
      opacity: 0.6;
      text-align: center;
      background: #000;
    }
    .drop-active h3 {
      margin: -0.5em 0 0;
      position: absolute;
      top: 50%;
      left: 0;
      right: 0;
      -webkit-transform: translateY(-50%);
      -ms-transform: translateY(-50%);
      transform: translateY(-50%);
      font-size: 40px;
      color: #fff;
      padding: 0;
    }
    .action-btn{
      .select-btn{
        top: 13px;
        padding: 7px 20px;
        background: #feae25;
        @include radius(4px);
        @media (max-width: 600px) {
          width: 100%;
          margin-bottom: 20px;
        }
      }
    }
    
  }
  #status-step{
    .status-row{
      margin: 5px 0 35px 30px;
      @media (max-width: 600px) {
        margin: 35px 0;
        padding: 0 5px;
      }
      h3{
        color: #222;
        margin-bottom: 8px;
        font-weight: 700;
        font-size: 14px;
      }
      .v-icon{
        font-size: 16px;
        margin-right: 6px;
      }
    }
    .uploaded-file{
      margin-bottom: 30px;
      h3{
        margin-bottom: 10px;
      }
      .v-subheader--inset{
        margin: 0 !important;
        background: #f9e7c8;
      }
      .v-list{
        @include radius(4px);
        background: #fff7ea;
        overflow: hidden;
      }
      .v-btn{
        margin: 0 2px;
      }
      .v-icon{
        font-size: 18px;
      }
    }
  }
}
</style>