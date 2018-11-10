<template>
   <v-content id="login">
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-3">
              <v-toolbar color="#fff" class="elevation-0">
                <v-toolbar-title>{{lang.login.heading}}</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form>
                  <v-text-field 
                  prepend-icon="fa-envelope" 
                  :label="lang.login.email" 
                  type="email"></v-text-field>
                  <v-text-field 
                  prepend-icon="fa-key" 
                  :label="lang.login.password" 
                  :append-icon="show ? 'visibility_off' : 'visibility'"
                  @click:append="show = !show"
                  :type="show ? 'text' : 'password'"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="#feae25" large class="elevation-0">{{lang.login.button}}</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
</template>

<script>
  export default {
    name: 'Login',
    data: function (){
      return{
        show: false,
        password: 'Password'
      }
    },
    computed: {
      lang(){ return this.$store.state.language }
    }
  }
</script>

<style lang="scss">
@import '../../assets/styles/vars';
@import '../../assets/styles/mixins';
#login{
 .container{
   background: $gray-background;
 }
 .v-card{
   padding: 15px 25px 20px;
   @include radius(4px);
   .v-btn{
     @include radius(4px);
   }
   .v-icon{
     font-size: 20px;
   }
 }
}
</style>