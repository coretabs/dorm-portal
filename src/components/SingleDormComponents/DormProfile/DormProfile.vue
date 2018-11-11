<template>
<div id="dorm-profile">
  <v-content>

    <v-parallax dark src="https://images.pexels.com/photos/1438072/pexels-photo-1438072.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260">
      <v-layout justify-center>

        <v-flex md8 xs10>
          <section id="dorm-banner">
            <h1>Alfam Dormitory</h1>
            <div>
              <v-icon>place</v-icon>
              <span>Kaleland street bla bla</span> - 
              <a href="#" @click.stop.prevent="showMap"> show map</a>
            </div>
          </section>
        </v-flex>

      </v-layout>
    </v-parallax>

  </v-content>
</div>
</template>

<script src="./DormProfile.js"></script>

<style src="./DormProfile.scss" lang="scss"></style>
