<template>
<header>

  <v-snackbar v-model="snackbar.trigger" :timeout="4000" top :color="snackbar.color">
    <span>{{snackbar.message}}</span>
    <v-btn flat color="white" @click="closeSnackbar">{{lang.snackbar.close}}</v-btn>
  </v-snackbar>

  <v-toolbar light flat fixed app>
    <!-- <v-toolbar-side-icon  @click.stop="drawer = !drawer"></v-toolbar-side-icon> -->
    <v-toolbar-title>
      <v-layout>
        <v-flex class="text-xs-center" v-if="!isSelectDormComponent && $route.path === '/manage' || $route.path === '/'">
          <v-btn flat class="mr-2 my-0" icon @click="toggleDrawer">
            <v-icon>menu</v-icon>
          </v-btn>
        </v-flex>
        <v-flex class="text-xs-center hidden-md-and-up" v-else>
          <v-btn flat class="mr-2 my-0" icon @click="$router.go(-1)">
            <v-icon>arrow_back</v-icon>
          </v-btn>
        </v-flex>
        <v-flex>
          <router-link to="/" id="logo">
            <img src="../../../assets/images/header/logo.png" alt="EMU">
            <span class="hidden-sm-and-down">{{lang.header.logo}}</span>
          </router-link>
        </v-flex>
      </v-layout>
    </v-toolbar-title>
    <v-spacer></v-spacer>

    <v-toolbar-items>

      <!-- Switching Dorms -->
      <v-menu transition="slide-y-transition" bottom offset-y v-if="$route.path === '/manage' && managerDorms.length > 1">
        <v-btn slot="activator" class="lang-btn" flat append-icon="expand_more">
          {{dormName}}
          <v-icon color="#ccc" right>expand_more</v-icon>
        </v-btn>
        <v-list>
          <v-list-tile v-for="(dorm, index) in managerDorms" :key="index" @click="switchDorms(dorm.id)">
            <v-list-tile-title>{{ dorm.name }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>

      <!-- Currency -->
      <v-menu id="currency-menu" transition="slide-y-transition" bottom offset-y v-if="$route.path !== '/reservation' && $route.path !== '/manage'" class="hidden-sm-and-down">
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
      <v-menu id="language-menu" transition="slide-y-transition" bottom offset-y class="hidden-sm-and-down">
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
                {{lang.header.dashboard}}
              </span>
              <span v-else>
                {{lang.header.status}}
              </span>
            </v-list-tile-title>
          </v-list-tile>
          <v-list-tile v-if="isAdmin" @click="dormProfile">
            <v-list-tile-title>
              {{lang.header.dormProfile}}
            </v-list-tile-title>
          </v-list-tile>
          <v-list-tile @click="logout">
            <v-list-tile-title>
              {{lang.header.logout}}
            </v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>

      <!-- <v-btn  flat dark class="status-btn" @click="logout">Logout</v-btn> -->
    </v-toolbar-items>

  </v-toolbar>

  <v-bottom-nav id="bottom-nav" :active.sync="activeBtn" :value="showNav" fixed color="#fff" v-if="$route.path != '/manage'">

    <v-layout align-center justify-space-between row fill-height>
      <v-flex xs4 class="text-xs-center">
        <v-menu transition="slide-y-transition" bottom offset-y>
          <v-btn large slot="activator" color="#1c3a70" class="lang-btn" flat append-icon="expand_more">
            <template>
              <span>Language</span>
              <v-icon>language</v-icon>
            </template>
          </v-btn>
          <v-list>
            <v-list-tile v-for="(language, index) in languages" :key="index" @click="changeLang(language.code)">
              <v-list-tile-title>{{ language.name }}</v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-menu>
      </v-flex>
      <v-flex xs4 v-if="$route.path === '/'">
        <v-btn large flat color="#1c3a70" @click="toggleDrawer">
          <template>
            <span>{{lang.bottomNav.filters}}</span>
            <v-icon v-if="!this.$store.state.drawer">fa-filter</v-icon>
            <v-icon v-else>fa-check</v-icon>
          </template>
        </v-btn>
      </v-flex>
      <v-flex xs4 v-else>
        <v-btn large flat color="#1c3a70" @click="$router.push('/')">
          <template>
            <span>Home</span>
            <v-icon>fa-home</v-icon>
          </template>
        </v-btn>
      </v-flex>
      <v-flex xs4 class="text-xs-center">
        <v-menu transition="slide-y-transition" bottom offset-y v-if="$route.path !== '/reservation' && $route.path !== '/manage'">
          <v-btn large slot="activator" color="#1c3a70" class="lang-btn" flat append-icon="expand_more">
            <template>
              <span>{{this.$store.state.currencyCode}}</span>
              <v-icon>fa-money-bill-wave</v-icon>
            </template>
          </v-btn>
          <v-list>
            <v-list-tile v-for="(currency, index) in currencies" :key="index" @click="changeCurrency(currency.code, currency.symbol)">
              <v-list-tile-title>{{ currency.code }}</v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-menu>
      </v-flex>
    </v-layout>

  </v-bottom-nav>

</header>
</template>

<script src="./Header.js"></script>

<style src="./Header.scss" lang="scss"></style>
