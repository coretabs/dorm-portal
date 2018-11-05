<template>
  <header>
    <v-toolbar light flat fixed>
      <!-- <v-toolbar-side-icon  @click.stop="drawer = !drawer"></v-toolbar-side-icon> -->
      <v-toolbar-title>
          <a href="#" id="logo">
            <img src="../../assets/images/header/logo.png" alt="EMU">
            <span>dormitories</span>
          </a>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="">
        <!-- <v-menu>
          <v-btn slot="activator" color="primary" dark >
            Dropdown
          </v-btn>
          <v-list>
            <v-list-tile v-for="(item, index) in items" :key="index" @click="" >
              <v-list-tile-title>{{ item.title }}</v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-menu> -->
        <v-btn flat dark class="status-btn">{{statusBtn}}</v-btn>
      </v-toolbar-items>
    </v-toolbar>
  </header>
</template>



<script>
  export default {
    name: 'HeaderComponent',
    data: function(){
      return{
        statusBtn: "Reservation Status"
      }
    }
  }
</script>

<style lang="scss">
@import '../../assets/styles/vars';
@import '../../assets/styles/mixins';
header{
  .v-toolbar__content{
    background-color: #fff;
    @include box-shadow(7px,0px,8px,rgba(0,0,0,0.4));
    #logo{
      display: flex;
      align-items: center;
      justify-content: center;
      text-decoration: none;
      color: $gray-color;
      outline: none;
      span{
        margin-left: 12px;
        padding-left: 8px;
        display: inline-block;
        border-left: 2px solid $light-gray-color;
        font-weight: 400;
        text-transform: uppercase;
      }
    }
    .status-btn{
      background-color: $primary-btn-color;
      height: 38px !important;
      @include radius(5px);
      text-transform: capitalize;
    }

  }
}
</style>