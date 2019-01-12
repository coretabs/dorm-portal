<template>
<v-flex md8 xs12 id="dorm-info">
  <v-card>
    <v-layout row wrap>
      <v-flex class="general-info" xs12 sm8>
        <v-tabs light slider-color="#7b7b7b">
          <v-tab ripple>{{lang.dormProfile.aboutUs}}</v-tab>
          <v-tab ripple>{{lang.dormProfile.features}}</v-tab>
          <v-tab ripple>{{lang.dormProfile.contactUs}}</v-tab>
          <v-tab-item lazy>
            <v-card flat>
              <v-card-text>
                <div class="pre-line">{{dorm.about}}</div>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item lazy>
            <v-card flat>
              <v-card-text>
                <div class="dorm-feature" v-for="feature in dorm.main_info.features" :key="feature.id">
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
                <p>{{lang.dormProfile.contactHeading}}:</p>
                <div class="contact-info">
                  <v-icon>fa-user</v-icon> <strong>{{lang.dormProfile.contactName}}:</strong> {{dorm.contact_name}}
                </div>
                <div class="contact-info">
                  <v-icon>fa-envelope</v-icon> <strong>{{lang.dormProfile.contactEmail}}:</strong> {{dorm.contact_email}}
                </div>
                <div class="contact-info">
                  <v-icon>fa-phone</v-icon> <strong>{{lang.dormProfile.contactPhone}}:</strong> {{dorm.contact_number}}
                </div>
                <div class="contact-info">
                  <v-icon>fa-fax</v-icon> <strong>{{lang.dormProfile.ContactFax}}:</strong> {{dorm.contact_fax}}
                </div>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs>
      </v-flex>
      <v-flex class="dorm-reviews" xs12 sm4>
        <div>
          <!-- TODO: Update reviews -->
          <div class="reviews-avarage">{{dorm.stars_average}}</div>

          <div class="review-details" v-if="isReviewed">
            <v-icon>fa-user-circle</v-icon>
            <span>{{maskName(review.student_name)}}</span>
            <v-rating v-model="review.stars" length="5" readonly background-color="rgba(0,0,0,0.2)" color="yellow accent-4" empty-icon="$vuetify.icons.ratingFull" half-increments dense>
            </v-rating>
            <p>
              {{review.description}}
            </p>
          </div>
          
          <div v-else class="review-details ot-5">
            <v-icon>fa-user-circle</v-icon>
            <span>{{lang.dormReview.yourName}}</span>
            <v-rating :v-model="5" length="5" readonly background-color="rgba(0,0,0,0.2)" color="yellow accent-4" empty-icon="$vuetify.icons.ratingFull" half-increments dense>
            </v-rating>
            <p>
              {{lang.dormReview.noReviews}}.
            </p>
          </div>
          <a href="#" @click.stop.prevent="showReviews(dorm.main_info.id)" v-if="isReviewed">{{dorm.number_of_reviews}} {{lang.dormReview.review}}</a>
        </div>
      </v-flex>
    </v-layout>
  </v-card>
  <v-dialog v-model="reviewsModel" lazy width="800px">
    <dorm-reviews :dormName="dorm.main_info.name" :reviews="dormReviews"></dorm-reviews>
  </v-dialog>
</v-flex>
</template>

<script src="./DormInfo.js"></script>

<style src="./DormInfo.scss" lang="scss"></style>
