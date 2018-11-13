<template>
<v-layout justify-start row wrap id="dorm-card">
  <v-flex md10 xs12>
    <v-card>
      <v-layout row wrap>

        <v-flex class="dorm-img" xs12 sm4>
          <v-img :src="dorm.cover" gradient="to top right, rgba(44,40,72,.4), rgba(44,40,72,.4)" height="100%" width="100%"></v-img>
        </v-flex>

        <v-flex class="dorm-details" xs12 sm8>

          <v-card-title class="pa-0">
            <h3 class="headline">
              <router-link to="/dorms/5" >{{dorm.name}}</router-link>
            </h3>
          </v-card-title>

          <v-layout class="dorm-rating" row>
            <v-rating v-model="dorm.stars" length="5" readonly background-color="rgba(0,0,0,0.2)" color="yellow accent-4" empty-icon="$vuetify.icons.ratingFull" half-increments dense>
            </v-rating>
            <a href="#" @click.stop.prevent="showReviews">{{dorm.number_of_reviews}} {{lang.dormCard.reviews}}</a>
          </v-layout>

          <v-layout class="dorm-address">
            <v-icon>place</v-icon>
            <span>{{dorm.address}}</span>
            <a href="#" @click.stop.prevent="showMap"> {{lang.dormCard.openMap}}</a>
          </v-layout>

          <template v-if=" roomsLeft <= 10 ">
            <v-layout class="dorm-warning">
              <v-icon>warning</v-icon>
              <span>{{roomsLeft}} {{lang.dormCard.roomsLeft}}</span>
            </v-layout>
          </template>

          <v-layout wrap class="dorm-features">

            <v-flex>
              <h3>{{lang.dormCard.dormFeatures}}:</h3>

              <v-tooltip top v-for="(feature, index) in popularFeatures" :key="index">
                <v-icon class="facility-icon" slot="activator">{{feature.icon}}</v-icon>
                <span>{{feature.name}}</span>
              </v-tooltip>

              <v-tooltip top>
                <v-icon class="facility-icon" slot="activator">more_horiz</v-icon>
                <span>{{lang.dormCard.more}}</span>
              </v-tooltip>

            </v-flex>

          </v-layout>

        </v-flex>

      </v-layout>

      <v-divider light></v-divider>

      <v-layout>
        <v-card-actions justify-center align-center>
          <div class="price-bar">

          </div>
        </v-card-actions>
      </v-layout>

    </v-card>

  </v-flex>
  <!-- Map Model -->
  <v-dialog v-model="mapModel" lazy width="800px">
    <dorm-map :longitude="dorm.geo_longitude" :latitude="dorm.geo_latitude"></dorm-map>
  </v-dialog>

  <!-- Reviews Model -->
  <v-dialog v-model="reviewsModel" lazy width="800px">
    <dorm-reviews></dorm-reviews>
  </v-dialog>

</v-layout>
</template>

<script src="./DormCard.js"></script>

<style src="./DormCard.scss" lang="scss"></style>
