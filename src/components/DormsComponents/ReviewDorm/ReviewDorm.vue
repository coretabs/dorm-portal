<template>
<v-content id="review">
  <v-container fluid fill-height>
    <v-layout  mt-5 justify-center>
      <v-flex xs12 sm8 md4>
        <v-card v-if="showForm" class="elevation-3">
          <v-form ref="form" lazy-validation>
            <v-card-text class="pa-5">
              <v-layout column class="text-xs-center">
                <h1 class="mb-3 pt-2">Rate Our Dormitory</h1>
                <p class="review-desc">If you enjoy staing in our Dormitory, please take a few seconds to rate your experience with us.</p>
              </v-layout>
              <v-layout column>
                <v-flex class="text-xs-center">
                  <v-rating v-model="rating" medium color="yellow darken-3" background-color="grey darken-1" empty-icon="$vuetify.icons.ratingFull" half-increments hover></v-rating>
                </v-flex>
                <v-flex class="mt-5">
                  <v-textarea v-model="comment" label="Write a Comment"></v-textarea>
                </v-flex>
              </v-layout>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="#feae25" :disabled="!rating" large class="elevation-0" @click.prevent="submitReview" :loading="loadingBtn">submit</v-btn>
            </v-card-actions>
          </v-form>
        </v-card>
        <v-card v-if="!showForm" class="elevation-3">
            <v-card-text>
              <v-layout column class="text-xs-center">
                <h1 class="mb-2">Thanks for Your review</h1>
              </v-layout>
             
            </v-card-text>
            <v-card-actions class="text-xs-center">
              <v-layout>
                <v-flex class="text-xs-center">
                 <v-btn color="#feae25" large class="elevation-0" to="/">Back Home</v-btn>
                </v-flex>
              </v-layout>
            </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
    
  </v-container>
</v-content>
</template>

<script src="./ReviewDorm.js"></script>

<style src="./ReviewDorm.scss" lang="scss"></style>
