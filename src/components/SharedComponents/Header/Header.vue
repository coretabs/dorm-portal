<template>
<header>

  <v-snackbar v-model="snackbar.trigger" :timeout="4000" top :color="snackbar.color">
    <span>{{snackbar.message}}</span>
    <v-btn flat color="white" @click="closeSnackbar">close</v-btn>
  </v-snackbar>
  
  <v-toolbar light flat fixed app >
    <!-- <v-toolbar-side-icon  @click.stop="drawer = !drawer"></v-toolbar-side-icon> -->
    <v-toolbar-title>
      <v-layout>
        <v-flex class="text-xs-center" v-if="!isSelectDormComponent && $route.path === '/manage' || $route.path === '/'">
          <v-btn flat class="mr-2 my-0" icon @click="toggleDrawer">
            <v-icon>menu</v-icon>
          </v-btn>
        </v-flex>
        <v-flex>
          <router-link to="/" id="logo">
            <img src="../../../assets/images/header/logo.png" alt="EMU">
            <span>{{lang.header.logo}}</span>
          </router-link>
        </v-flex>
      </v-layout>
    </v-toolbar-title>
    <v-spacer></v-spacer>

    <v-toolbar-items>

      <!-- Switching Dorms -->
      <v-menu id="currency-menu" transition="slide-y-transition" bottom offset-y v-if="$route.path === '/manage' && managerDorms.length > 1">
        <v-btn slot="activator" class="lang-btn" flat append-icon="expand_more">
          Switch Dorms
          <v-icon color="#ccc" right>expand_more</v-icon>
        </v-btn>
        <v-list>
          <v-list-tile v-for="(dorm, index) in managerDorms" :key="index" @click="switchDorms(dorm.id)">
            <v-list-tile-title>{{ dorm.name }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>

      <!-- Currency -->
      <v-menu id="currency-menu" transition="slide-y-transition" bottom offset-y v-if="$route.path !== '/reservation' && $route.path !== '/manage'">
        <v-btn slot="activator" class="lang-btn" flat append-icon="expand_more">
          {{this.$store.state.currencyCode}}
          <v-icon color="#ccc" right>expand_more</v-icon>
        </v-btn>
        <v-list>
          <v-list-tile v-for="(currency, index) in currencies" :key="index" @click="changeCurrency(currency.code, currency.symbol)">
            <v-list-tile-title>{{ currency.code }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>
      <!-- language -->
      <v-menu id="language-menu" transition="slide-y-transition" bottom offset-y>
        <v-btn slot="activator" class="lang-btn" flat append-icon="expand_more">
          <v-icon color="#666">language</v-icon>
          <v-icon color="#ccc" right>expand_more</v-icon>
        </v-btn>
        <v-list>
          <v-list-tile v-for="(language, index) in languages" :key="index" @click="changeLang(language.code)">
            <v-list-tile-title>{{ language.name }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>
      <!-- check status -->

      <v-btn v-if="!isLogin" flat dark class="status-btn" to="/login">{{lang.header.button}}</v-btn>
      <v-menu v-else id="language-menu" class="status-btn" transition="slide-y-transition" bottom offset-y>
        <v-btn dark slot="activator" class="lang-btn pl-3" flat append-icon="expand_more">
          <span>{{userName}}</span>
          <v-icon color="#ccc">expand_more</v-icon>
        </v-btn>
        <v-list>
          <v-list-tile @click="userRedirect">
            <v-list-tile-title>
              <span v-if="isAdmin">
                Dashboard
              </span>
              <span v-else>
                Status
              </span>
            </v-list-tile-title>
          </v-list-tile>
          <v-list-tile v-if="isAdmin" @click="dormProfile">
            <v-list-tile-title>
              Dorm Profile
            </v-list-tile-title>
          </v-list-tile>
          <v-list-tile @click="logout">
            <v-list-tile-title>
              Logout
            </v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>

      <!-- <v-btn  flat dark class="status-btn" @click="logout">Logout</v-btn> -->
    </v-toolbar-items>

  </v-toolbar>

  <v-bottom-nav id="bottom-nav" :active.sync="activeBtn" :value="showNav" fixed color="#fff" v-if="$route.path === '/'">

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
