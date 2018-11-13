<template>
<v-flex md8 xs12 id="dorm-info">
  <v-card>
    <v-layout row wrap>

      <v-flex class="general-info" xs12 sm8>

        <v-tabs light slider-color="#7b7b7b">
          <v-tab ripple>About us</v-tab>
          <v-tab ripple>Our Features</v-tab>
          <v-tab ripple>Contact Us</v-tab>
          <v-tab-item lazy>
            <v-card flat>
              <v-card-text>
                <div class="pre-line">{{history}}</div>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item lazy>
            <v-card flat>
              <v-card-text>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim ve
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item class="contact">
            <v-card flat>
              <v-card-text>
                <p>You can contact us through:</p>
                <div class="contact-info"><v-icon>fa-envelope</v-icon> {{contact_email}}</div>
                <div class="contact-info"><v-icon>fa-phone</v-icon> {{contact_number}}</div>
              </v-card-text>
            </v-card>
          </v-tab-item>

        </v-tabs>

      </v-flex>

      <v-flex class="dorm-reviews" xs12 sm4>
        <div>
          <div class="reviews-avarage">{{reviews_average}}</div>
          <div class="review-details">
            <v-icon>fa-user-circle</v-icon>
            <span>Mohammed Alhakem</span>
            <v-rating v-model="reviews_average" length="5" readonly background-color="rgba(0,0,0,0.2)" color="yellow accent-4" empty-icon="$vuetify.icons.ratingFull" half-increments dense>
            </v-rating>
            <p>
              The place is good especially when it comes to its location and cleanliness. Staff are amazing and very friendly. It is very good compared to the price.
            </p>
            <div class="dots"></div>
            <a href="#">126 reviews</a>
          </div>
        </div>
      </v-flex>

    </v-layout>

  </v-card>

</v-flex>
</template>

<script src="./DormInfo.js"></script>

<style src="./DormInfo.scss" lang="scss"></style>
