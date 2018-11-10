<template>
  <header>
    <v-toolbar light flat fixed app :clipped-left="$vuetify.breakpoint.lgAndUp">
      <!-- <v-toolbar-side-icon  @click.stop="drawer = !drawer"></v-toolbar-side-icon> -->
      <v-toolbar-title>
        <router-link to="/" id="logo">
            <img src="../../assets/images/header/logo.png" alt="EMU">
            <span>{{lang.header.logo}}</span>
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>

      <v-toolbar-items>
        <!-- Currency -->
        <v-menu transition="slide-y-transition" bottom offset-y >
          <v-btn slot="activator" class="lang-btn" flat append-icon="expand_more">
            USD<v-icon color="#ccc" right>expand_more</v-icon>
          </v-btn>
          <v-list>
            <v-list-tile v-for="(currency, index) in currencies" :key="index"  >
              <v-list-tile-title>{{ currency.code }}</v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-menu>
        <!-- language -->
        <v-menu transition="slide-y-transition" bottom offset-y >
          <v-btn slot="activator" class="lang-btn" flat append-icon="expand_more">
            <v-icon color="#666">language</v-icon> <v-icon color="#ccc" right>expand_more</v-icon>
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
  </header>
</template>

<script>
export default {
  name: "HeaderComponent",
  data: function() {
    return {
      currencies: [{ symbol: "$", code: "USD" }, { symbol: "₺", code: "TL" }],
      languages: [
        { symbol: "English", code: "en" },
        { symbol: "Turkish", code: "tr" }
      ]
    };
  },
  methods: {
    changeLang(lang) {
      this.$store.state.language = lang;
      localStorage.setItem("lang", lang);
    }
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
header {
  .v-toolbar__content {
    background-color: #fff;
    @include box-shadow(0px, 0px, 8px, rgba(0, 0, 0, 0.4));
    #logo {
      display: flex;
      align-items: center;
      justify-content: center;
      text-decoration: none;
      color: $gray-color;
      outline: none;
      span {
        margin-left: 12px;
        padding-left: 8px;
        display: inline-block;
        border-left: 2px solid $light-gray-color;
        font-weight: 400;
        text-transform: uppercase;
      }
    }
    .status-btn {
      background-color: $primary-btn-color;
      text-transform: capitalize;
    }
    .lang-btn {
      padding: 0 10px;
    }
  }
}
</style>