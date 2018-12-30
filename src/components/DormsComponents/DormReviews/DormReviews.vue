<template>
<v-container id="reviews" grid-list-sm>
  <v-layout row wrap>
    <v-flex xs12>
      <h2>{{dormName}} {{lang.dormCard.reviews}}:</h2>
    </v-flex>

    <v-flex xs12>
      <div id="review" v-for="(review,index) in reviews" :key="index">
        <span class="review-name">{{review.student_name}}</span>
        <span class="review-date"> on {{review.review_creation_date}}</span>

        <v-rating v-model="review.stars" length="5" readonly background-color="rgba(0,0,0,0.2)" color="yellow accent-4" empty-icon="$vuetify.icons.ratingFull" half-increments dense>
        </v-rating>
        <p class="review-description">{{review.description}}</p>
      </div>
    </v-flex>

  </v-layout>
</v-container>
</template>

<script src="./DormReviews.js" ></script>

<style src="./DormReviews.scss" lang="scss"></style>
