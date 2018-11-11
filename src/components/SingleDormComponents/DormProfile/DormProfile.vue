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
              <swiper :options="swiperOption">
                <swiper-slide v-for="(photo,i) in photos" :key="i" >
                  <template v-if="photo.is_3d">
                     <img src="../../../assets/images/dormprofile/360.png" @click="sendPhotoUrl(photo.src, photo.is_3d)">
                  </template> 
                  <template v-else>
                    <v-img :src="photo.src" gradient="to top right, rgba(255,255,255,.2), rgba(255,255,255,0)" @click="sendPhotoUrl(photo.src, photo.is_3d)"></v-img>
                  </template> 
                </swiper-slide>
              </swiper> 
          </section>
          <v-dialog v-model="lightbox" lazy width="800px">
            <v-card>
              <v-card-text>
                <template v-if="iframe">
                  <iframe height="500px" width="100%" allowfullscreen="true" :src="lightboxPhotoUrl" frameBorder="0"></iframe>
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
    <div>
      
    </div>
  </v-content>
</div>
</template>

<script src="./DormProfile.js"></script>

<style src="./DormProfile.scss" lang="scss"></style>
