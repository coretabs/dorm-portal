<template>
<div id="dorm-profile">
  <v-content>

    <v-parallax dark :src="cover">
      <v-layout justify-center>

        <v-flex md8 xs10>
          <section id="dorm-banner">
            <h1>{{name}}</h1>
            <div>
              <v-icon>place</v-icon>
              <span>{{address}}</span> - 
              <a href="#" @click.stop.prevent="showMap"> show map</a>
            </div>
          </section>
          <section id="dorm-photos">
              <div v-for="n in 15" :key="n"></div>
          </section>
        </v-flex>

      </v-layout>
    </v-parallax>

  </v-content>
</div>
</template>

<script src="./DormProfile.js"></script>

<style src="./DormProfile.scss" lang="scss"></style>
