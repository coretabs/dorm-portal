<template>
<header>
  <v-toolbar light flat fixed app :clipped-left="$vuetify.breakpoint.lgAndUp">
    <!-- <v-toolbar-side-icon  @click.stop="drawer = !drawer"></v-toolbar-side-icon> -->
    <v-toolbar-title>
      <router-link to="/" id="logo">
        <img src="../../../assets/images/header/logo.png" alt="EMU">
        <span>{{lang.header.logo}}</span>
      </router-link>
    </v-toolbar-title>
    <v-spacer></v-spacer>

    <v-toolbar-items>
      <!-- Currency -->
      <v-menu id="currency-menu" transition="slide-y-transition" bottom offset-y>
        <v-btn slot="activator" class="lang-btn" flat append-icon="expand_more">
          {{this.$store.state.currency}}<v-icon color="#ccc" right>expand_more</v-icon>
        </v-btn>
        <v-list>
          <v-list-tile v-for="(currency, index) in currencies" :key="index" @click="changeCurrency(currency.code, currency.symbol)">
            <v-list-tile-title>{{ currency.code }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>
      <!-- language -->
      <v-menu id="language-menu"  transition="slide-y-transition" bottom offset-y>
        <v-btn slot="activator" class="lang-btn" flat append-icon="expand_more">
          <v-icon color="#666">language</v-icon>
          <v-icon color="#ccc" right>expand_more</v-icon>
        </v-btn>
        <v-list>
          <v-list-tile v-for="(language, index) in languages" :key="index" @click="changeLang(language.code)">
            <v-list-tile-title>{{ language.symbol }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>
      <!-- check status -->
      <v-btn flat dark class="status-btn" to="/login">{{lang.header.button}}</v-btn>
    </v-toolbar-items>

  </v-toolbar>

  <v-bottom-nav id="bottom-nav" :active.sync="activeBtn" :value="showNav" fixed color="#fff">

    <v-btn flat color="teal" @click="toggleDrawer">
      <template>
        <span>Filters</span>
        <v-icon>fa-filter</v-icon>
      </template>
    </v-btn>

  </v-bottom-nav>

</header>
</template>

<script src="./Header.js"></script>

<style src="./Header.scss" lang="scss"></style>
