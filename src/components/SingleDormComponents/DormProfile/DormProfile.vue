<template>
<div id="dorm-profile">
  <v-content>

    <v-parallax height="450" dark :src="cover">
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
            <swiper :options="swiperOption">
              <swiper-slide v-for="(photo,i) in photos" :key="i">
                <template v-if="photo.is_3d">
                  <img class="elevation-3" src="../../../assets/images/dormprofile/360.png" @click="sendPhotoUrl(photo.src, photo.is_3d)">
                  </template>
                  <template v-else>
                    <v-img :src="photo.src" gradient="to top right, rgba(255,255,255,0), rgba(0,0,0,0.1)" @click="sendPhotoUrl(photo.src, photo.is_3d)"></v-img>
                  </template>
              </swiper-slide>
            </swiper>
          </section>
          <v-dialog v-model="lightbox" lazy width="800px">
            <v-card>
              <v-card-text>
                <template v-if="iframe">
                  <iframe height="450px" width="100%" allowfullscreen="true" :src="lightboxPhotoUrl" frameBorder="0"></iframe>
                </template>
                <template v-else>
                  <v-img :src="lightboxPhotoUrl" height="100%" width="100%"></v-img>
                </template>
              </v-card-text>
            </v-card>
          </v-dialog>
        </v-flex>
      </v-layout>
    </v-parallax>

    <v-layout justify-center row wrap>

      <dorm-info></dorm-info>

      <v-flex id="filter-results-number" md8>
        <v-layout justify-center row wrap>
          <v-flex md10>
            <p>
              <v-icon>fa-filter</v-icon>
              We have found 4 rooms matching your search in this dorm
            </p>
          </v-flex>
          <v-flex md2>
            <v-btn class="elevation-0"><v-icon>fa-search</v-icon> Do anther search</v-btn>
          </v-flex>
        </v-layout>
      </v-flex>
   
      <room-card v-for="n in 2" :key="n"></room-card>
      
    </v-layout>

  </v-content>
  <!-- Map Model -->
  <v-dialog v-model="mapModel" lazy width="800px">
    <dorm-map :longitude="geo_longitude" :latitude="geo_latitude"></dorm-map>
  </v-dialog>
</div>
</template>

<script src="./DormProfile.js"></script>

<style src="./DormProfile.scss" lang="scss"></style>
