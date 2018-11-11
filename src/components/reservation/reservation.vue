<template>
   <v-content id="reservation">
      <v-container fluid fill-height>
        <v-layout justify-center>
          <v-flex xs12 sm8 md8>
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
                               <p>Please make a transiction to one of our bank accounts, then upload the receipt below.</p>
                              <v-form>
                                <v-text-field 
                                :label="lang.confirmPayment.file" 
                                type="file"></v-text-field>
                              </v-form>
                            </v-card-text>
                            <v-card-actions>
                              <v-spacer></v-spacer>
                              <v-btn color="#feae25" class="elevation-0" @click="e1 = 2">{{lang.signup.button}}</v-btn>
                            </v-card-actions>
                          </v-card>
                        </div>
                      </v-flex>
                    </v-layout>
                  
              </v-stepper-content>

              <v-stepper-content step="3">
                <v-card
                  class="mb-5"
                  color="grey lighten-1"
                  height="200px"
                ></v-card>

                <v-btn
                  color="primary"
                  @click="e1 = 1"
                >
                  Continue
                </v-btn>

                <v-btn flat>Cancel</v-btn>
              </v-stepper-content>
            </v-stepper-items>
          </v-stepper>
          </v-flex>

        </v-layout>
      </v-container>
    </v-content>
</template>

<script>
export default {
  name: "Reservation",
  data: function() {
    return {
      e1: 2,
      show: false,
      password: "Password"
    };
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
    .v-expansion-panel__container{
      @include radius(4px);
    }
  }
  #upload-file{
  }
}
</style>