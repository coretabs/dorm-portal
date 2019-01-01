<template>
<div id="manage-reservations" class="mt-2">
  <v-card>
    <v-card-text>
      <v-layout id="statistics-cards" wrap>

        <v-flex xs6 md2>
          <div @click="filterByStatus()">
            <v-icon>fa-layer-group</v-icon>
            <h3>{{lang.manageResrevations.all}}</h3>
            <span>{{reservationCount}}</span>
          </div>
        </v-flex>

        <v-flex xs6 md2>
          <div @click="filterByStatus(3)">
            <v-icon>fa-hourglass-end</v-icon>
            <h3>{{lang.manageResrevations.wating}}</h3>
            <span>{{reservationData.waiting_for_manager_action_reservations}}</span>
          </div>
        </v-flex>

        <v-flex xs6 md2>
          <div @click="filterByStatus(0)">
            <v-icon>fa-history</v-icon>
            <h3>{{lang.manageResrevations.pending}}</h3>
            <span>{{reservationData.pending_reservations}}</span>
          </div>
        </v-flex>

        <v-flex xs6 md2>
          <div @click="filterByStatus(2)">
            <v-icon>fa-check</v-icon>
            <h3>{{lang.manageResrevations.confirmed}}</h3>
            <span>{{reservationData.confirmed_reservations}}</span>
          </div>
        </v-flex>

        <v-flex xs6 md2>
          <div @click="filterByStatus(1)">
            <v-icon>fa-ban</v-icon>
            <h3>{{lang.manageResrevations.rejected}}</h3>
            <span>{{reservationData.rejected_reservations}}</span>
          </div>
        </v-flex>

        <v-flex xs6 md2>
          <div @click="filterByStatus(5)">
            <v-icon>fa-calendar-times</v-icon>
            <h3>{{lang.manageResrevations.Expired}}</h3>
            <span>{{reservationData.expired_reservations}}</span>
          </div>
        </v-flex>

      </v-layout>

      <v-layout id="receipts-records" wrap>
        <v-flex xs12>
          <v-card class="elevation-0">
            <v-card-title>
              <h2>{{lang.manageResrevations.heading}}</h2>
              <v-spacer></v-spacer>
              <v-text-field v-model="search" prepend-icon="search" @input="filterByStatus()" :label="lang.manageResrevations.search" single-line hide-details></v-text-field>
            </v-card-title>

            <v-data-table :headers="headers" :items="reservations" :search="search" :rows-per-page-items="rowsPerPage" :pagination.sync="pagination">

              <template slot="items" slot-scope="props">
                <tr>
                  <td class="text-xs-left">{{ props.item.room_price_currency }}{{ props.item.room_price }}</td>
                  <td class="text-xs-left">
                    <v-menu :close-on-content-click="false" transition="slide-y-transition" :nudge-width="150" offset-y v-if="props.item.receipts.length">
                      <v-btn class="receipts-btn" slot="activator" depressed flat>
                        {{lang.manageResrevations.download}}
                        <v-icon color="#999">expand_more</v-icon>
                      </v-btn>
                      <v-card class="v-list-files">
                        <v-list v-for="(receipt,i) in props.item.receipts" :key="i">
                          <v-list-tile avatar>

                            <v-list-tile-content>
                              <v-list-tile-title>
                                <a :href="receipt.url" download>{{lang.manageResrevations.receipt}} {{i+1}}</a>
                              </v-list-tile-title>
                              <v-list-tile-sub-title>
                                {{receipt.upload_receipt_date}}
                              </v-list-tile-sub-title>
                            </v-list-tile-content>

                            <v-list-tile-action>
                              <a :href="receipt.url" download>
                              <v-icon class="grey--text text--lighten-1">fa-file-download</v-icon>
                            </a>
                            </v-list-tile-action>

                          </v-list-tile>

                        </v-list>

                      </v-card>
                    </v-menu>
                    <div v-else class="grey--text text--darken-5 ml-1">{{lang.manageResrevations.noFiles}}</div>

                  </td>
                  <td class="text-xs-left">
                    <span v-if="props.item.status == 0">Pending</span>
                    <span v-else-if="props.item.status == 1">Rejected</span>
                    <span v-else-if="props.item.status == 2">Confirmed</span>
                    <span v-else-if="props.item.status == 3">Wating Action</span>
                    <span v-else-if="props.item.status == 4">Updated</span>
                    <span v-else>Expired</span>
                  </td>
                  <td class="text-xs-left">{{ props.item.last_update_date }}</td>
                  <td class="text-xs-left">{{ props.item.student_name }}</td>
                  <td class="text-xs-left">{{ props.item.student_email }}</td>
                  <td class="text-xs-left">{{ props.item.reservation_creation_date }}</td>
                  <td class="text-xs-left">{{ props.item.confirmation_deadline_date }}</td>
                  <td class="text-xs-left layout pl-3">
                    <v-tooltip top>
                      <v-btn slot="activator" @click="props.expanded = !props.expanded" flat icon>
                        <v-icon color="#677889">fa-info-circle</v-icon>
                      </v-btn>
                      <span>{{lang.manageResrevations.moreInfo}}</span>
                    </v-tooltip>
                    <v-btn depressed @click="updateStatus(props.item)" v-if="props.item.status != 2" color="green" dark>
                      {{lang.manageResrevations.updateStatus}}
                    </v-btn>
                    <v-btn depressed :disabled="props.item.is_reviewed || !props.item.is_reviewable" v-if="props.item.status == 2" @click="askForReview(props.item.id)">
                      <span v-if="props.item.is_reviewed">{{lang.manageResrevations.reviewd}}</span>
                      <span v-else>{{lang.manageResrevations.askForReview}}</span>
                    </v-btn>
                    
                    <v-tooltip top>
                      <v-btn slot="activator" icon depressed @click="updateStatus(props.item)" v-if="props.item.status == 2">
                        <v-icon small class="grey--text">fa-pen</v-icon>
                      </v-btn>
                      <span>{{lang.manageResrevations.updateStatus}}</span>
                    </v-tooltip>
                  </td>
                </tr>
              </template>
              <template slot="expand" slot-scope="props">
                <v-card flat>
                  <v-card-text>
                    <v-layout>
                      <v-flex md6>
                        <v-layout fill-height class="details-room">
                          <v-flex class="details-model__info">
                            <h3>{{lang.AddnewRoom.roomType}}:</h3>
                            <span>{{props.item.room_type}}</span>
                          </v-flex>
                          <v-flex class="details-model__info">
                            <h3>{{lang.AddnewRoom.allowedPeople}}:</h3>
                            <span v-if="props.item.room_people_allowed_number < 4">
                              <v-icon v-for="n in props.item.room_people_allowed_number" small :key="n" class="mr-1">fa-user</v-icon>
                            </span>
                            <span v-else>
                              <v-icon>fa-user</v-icon>
                              X {{props.item.room_people_allowed_number}}
                            </span>
                          </v-flex>
                          <v-flex class="details-model__info">
                            <h3>{{lang.AddnewRoom.duration}}:</h3>
                            <span>{{props.item.room_duration}}</span>
                          </v-flex>
                        </v-layout>
                      </v-flex>
                      <v-flex md6>
                        <v-layout fill-height column class="details-model__info">
                          <h3>{{lang.manageResrevations.statusCmt}}:</h3>
                          <span v-if="props.item.follow_up_message">{{props.item.follow_up_message}}</span>
                          <span v-else>{{lang.manageResrevations.noCmt}}</span>
                        </v-layout>
                      </v-flex>

                    </v-layout>

                  </v-card-text>
                </v-card>
              </template>
              <v-alert slot="no-results" :value="true" color="error" icon="warning">
                {{lang.manageResrevations.searchResults}} "{{ search }}".
              </v-alert>

            </v-data-table>
          </v-card>
        </v-flex>
      </v-layout>

    </v-card-text>
  </v-card>

  <v-layout row justify-center>
    <v-dialog v-model="showUpdateStatus" persistent max-width="600px">
      <v-card lazy>
        <v-card-text>
          <v-container grid-list-md>
            <h2 class="mb-4">{{lang.manageResrevations.updateStatusHeading}} </h2>
            <v-form ref="form" lazy-validation>

              <v-layout wrap>
                <v-flex xs12>
                  <v-select prepend-icon="fa-pen" :items="status" v-model="currentStatus" :label="lang.manageResrevations.statusLabel" @change="setStatusIndex" required :rules="statusRules"></v-select>
                </v-flex>
                <v-flex xs12 v-if="statusIndex == 0">
                  <v-menu ref="menu" :close-on-content-click="false" v-model="menu" :nudge-right="40" :return-value.sync="date" lazy transition="scale-transition" offset-y full-width min-width="290px">
                    <v-text-field :required="setStatusIndex == 0" :rules="requiredRules" prepend-icon="fa-calendar" slot="activator" v-model="date" label="Deadline" readonly></v-text-field>
                    <v-date-picker v-model="date" no-title @input="$refs.menu.save(date); menu = false" scrollable>

                    </v-date-picker>
                  </v-menu>
                </v-flex>
                <v-flex xs12>
                  <v-textarea prepend-icon="fa-envelope" :label="lang.manageResrevations.noteLabel" v-model="followUpMessage" required :rules="requiredRules"></v-textarea>
                </v-flex>

              </v-layout>
            </v-form>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey darken-1" flat @click="close">{{lang.shared.close}}</v-btn>
          <v-btn color="green darken-1" dark depressed @click="submit" :loading="loadingBtn">{{lang.shared.update}}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>

  <v-dialog v-model="isReviewRequestSent" width="500" lazy>
    <v-card >
      <v-card-text class="text-xs-center subheading pt-5 pb-4">
        <v-icon large color="success" class="mb-4 ">fa-check-circle</v-icon>
        <h3>
          {{lang.manageResrevations.sentReviewRequestMsg}}
        </h3>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn class="elevation-0" @click="isReviewRequestSent = false">{{lang.shared.close}}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</div>
</template>

<script src="./ManageReservations.js"></script>

<style src="./ManageReservations.scss" lang="scss"></style>
