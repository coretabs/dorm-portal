<template>
<v-flex md8 xs12 id="dorm-info">
  <v-card>
    <v-layout row wrap>
      <v-flex class="general-info" xs12 sm8>
        <v-tabs light slider-color="#7b7b7b">
          <v-tab ripple>About us</v-tab>
          <v-tab ripple>Features</v-tab>
          <v-tab ripple>Contact Us</v-tab>
          <v-tab-item lazy>
            <v-card flat>
              <v-card-text>
                <!-- TODO: Update about object -->
                <div class="pre-line">{{dorm.about}}</div>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item lazy>
            <v-card flat>
              <v-card-text>
                <div class="dorm-feature" v-for="(feature,index) in dorm.main_info.features" :key="index">
                  <v-icon v-if="feature.icon">{{feature.icon}}</v-icon>
                  <v-icon v-else>fa-check</v-icon>
                  <span>{{feature.name}}</span>
                </div>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item class="contact">
            <v-card flat>
              <v-card-text>
                <p>You can contact us through:</p>
                <div class="contact-info">
                  <v-icon>fa-user</v-icon> <strong>Name:</strong> {{dorm.contact_name}}
                </div>
                <div class="contact-info">
                  <v-icon>fa-envelope</v-icon> <strong>Email:</strong> {{dorm.contact_email}}
                </div>
                <div class="contact-info">
                  <v-icon>fa-phone</v-icon> <strong>Phone:</strong> {{dorm.contact_number}}
                </div>
                <div class="contact-info">
                  <v-icon>fa-fax</v-icon> <strong>Fax:</strong> {{dorm.contact_fax}}
                </div>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs>
      </v-flex>
      <v-flex class="dorm-reviews" xs12 sm4>
        <div>
          <!-- TODO: Update reviews -->
          <div class="reviews-avarage">{{reviews_average}}</div>
              <div class="review-details">
                <v-icon>fa-user-circle</v-icon>
                <span>Mohammed Alhakem</span>
                <v-rating v-model="reviews_average" length="5" readonly background-color="rgba(0,0,0,0.2)" color="yellow accent-4" empty-icon="$vuetify.icons.ratingFull" half-increments dense>
                </v-rating>
                <p>
                  The place is good especially when it comes to its location and cleanliness. Staff are amazing and very friendly. It is very good compared to the price.
                </p>
              </div>
          <a href="#">126 reviews</a>
        </div>
      </v-flex>
    </v-layout>
  </v-card>
</v-flex>
</template>

<script src="./DormInfo.js"></script>

<style src="./DormInfo.scss" lang="scss"></style>
