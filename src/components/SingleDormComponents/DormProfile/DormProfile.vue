<template>
<div id="dorm-profile">
  <v-content>
    <v-parallax height="450" dark :src="dorm.main_info.cover">
      <v-layout justify-center>
        <v-flex md8 xs10>
          <section id="dorm-banner">
            <h1>{{dorm.main_info.name}}</h1>
            <div>
              <v-icon>place</v-icon>
              <span>{{dorm.main_info.address}}</span> -
              <a href="#" @click.stop.prevent="showMap"> {{lang.dormProfile.showMap}}</a>
            </div>
          </section>
          <section id="dorm-photos">
            <swiper :options="swiperOption">
              <!-- TODO: Update photos -->
              <swiper-slide v-for="(photo,i) in dorm.photos" :key="i">
                <template v-if="photo.is_3d">
                  <img src="../../../assets/images/dormprofile/360.png" @click="sendPhotoUrl(photo.url, photo.is_3d)">
                  </template>
                  <template v-else>
                    <v-img :src="photo.url" gradient="to top right, rgba(255,255,255,0), rgba(0,0,0,0.1)" @click="sendPhotoUrl(photo.url, photo.is_3d)">
                      <v-layout slot="placeholder" fill-height align-center justify-center ma-0>
                        <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
                      </v-layout>
                    </v-img>
                  </template>
              </swiper-slide>
            </swiper>
          </section>
          <v-dialog v-model="lightbox" lazy width="800px">
            <v-card>
              <v-card-text>
                <template v-if="iframe">
                  <div class="iframe-loader">
                    <v-progress-circular :size="50" color="grey" indeterminate></v-progress-circular>
                  </div>
                  <iframe class="iframe-holder" height="450px" width="100%" allowfullscreen="true" :src="lightboxPhotoUrl" frameBorder="0"></iframe>
                </template>
                <template v-else>
                  <v-img :src="lightboxPhotoUrl" height="100%" width="100%">
                    <v-layout slot="placeholder" fill-height align-center justify-center ma-0>
                      <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
                    </v-layout>
                  </v-img>
                </template>
              </v-card-text>
            </v-card>
          </v-dialog>
        </v-flex>
      </v-layout>
    </v-parallax>

    <v-layout justify-center row wrap mb-5>

      <dorm-info :dorm="dorm"></dorm-info>

      <room-card  v-for="(room,i) in dorm.room_characteristics" :room="room" :key="i"></room-card>

    </v-layout>

  </v-content>
  <!-- Map Model -->
  <v-dialog v-model="mapModel" lazy width="800px">
    <dorm-map :longitude="dorm.main_info.geo_longitude" :latitude="dorm.main_info.geo_latitude"></dorm-map>
  </v-dialog>

  <template v-if="checkSavedRoom">
    <single-room-card></single-room-card>
  </template>

</div>
</template>

<script src="./DormProfile.js"></script>

<style src="./DormProfile.scss" lang="scss"></style>
