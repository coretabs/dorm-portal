<template>
<div id="manage-reservations">
  <v-card>
    <v-card-text>
      <v-layout id="statistics-cards" wrap>

        <v-flex xs6 md2>
          <div @click="filterStatus('')">
            <h3>{{lang.manageResrevations.all}}</h3>
            <span>25</span>
          </div>
        </v-flex>

        <v-flex xs6 md2>
          <div @click="filterStatus(lang.manageResrevations.wating)">
            <h3>{{lang.manageResrevations.wating}}</h3>
            <span>25</span>
          </div>
        </v-flex>

        <v-flex xs6 md2>
          <div @click="filterStatus(lang.manageResrevations.pending)">
            <h3>{{lang.manageResrevations.pending}}</h3>
            <span>12</span>
          </div>
        </v-flex>

        <v-flex xs6 md2>
          <div @click="filterStatus(lang.manageResrevations.confirmed)">
            <h3>{{lang.manageResrevations.confirmed}}</h3>
            <span>125</span>
          </div>
        </v-flex>

        <v-flex xs6 md2>
          <div @click="filterStatus(lang.manageResrevations.rejected)">
            <h3>{{lang.manageResrevations.rejected}}</h3>
            <span>35</span>
          </div>
        </v-flex>

        <v-flex xs6 md2>
          <div @click="filterStatus(lang.manageResrevations.unpaid)">
            <h3>{{lang.manageResrevations.unpaid}}</h3>
            <span>28</span>
          </div>
        </v-flex>

      </v-layout>

      <v-layout id="receipts-records" wrap>
        <v-flex xs12>
          <v-card class="elevation-0">
            <v-card-title>
              <strong>{{lang.manageResrevations.heading}}</strong>
              <v-spacer></v-spacer>
              <v-text-field v-model="search" append-icon="search" label="Search" single-line hide-details></v-text-field>
            </v-card-title>
            <v-data-table :headers="headers" :items="reservations" :search="search">
              <template slot="items" slot-scope="props">
                <td class="text-xs-left">${{ props.item.amount }}</td>
                <td class="text-xs-left">

                  <v-menu offset-y>
                    <v-btn class="receipts-btn" slot="activator" depressed flat>
                      {{lang.manageResrevations.download}}
                      <v-icon color="#999">expand_more</v-icon>
                    </v-btn>
                    <v-list>
                      <v-list-tile v-for="(receipt,i) in props.item.receipts" :key="i">
                        <a :href="receipt" download>{{lang.manageResrevations.receipt}} {{i+1}}</a>
                      </v-list-tile>
                    </v-list>
                  </v-menu>

                </td>
                <td class="text-xs-left">{{ props.item.status }}</td>
                <td class="text-xs-left">{{ props.item.name }}</td>
                <td class="text-xs-left">{{ props.item.email }}</td>
                <td class="text-xs-left">{{ props.item.submittedOn }}</td>
                <td class="text-xs-left">{{ props.item.deadline }}</td>
                <td class="text-xs-left layout px-0">
                  <v-btn @click="showMoreDetails(props.item)" flat icon>
                    <v-icon color="#ccc">fa-info-circle</v-icon>
                  </v-btn>
                  <v-btn depressed @click="updateStatus(props.item)" v-if="props.item.status.toLowerCase() != lang.manageResrevations.confirmed.toLowerCase()" color="green" dark>{{lang.manageResrevations.updateStatus}}</v-btn>
                  <v-btn depressed v-else>{{lang.manageResrevations.askForReview}}</v-btn>
                </td>
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

  <v-layout>
    <v-dialog v-model="showDetails" max-width="400">
      <v-card>
        <v-card-text>
          <div class="details-model__info">
            <h3>Room Type:</h3>
            <span>{{details.roomType}}</span>
          </div>
          <div class="details-model__info">
            <h3>Staying Duration:</h3>
            <span>{{details.duration}}</span>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" flat="flat" @click="showDetails = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>

  <v-layout row justify-center>
    <v-dialog v-model="showUpdateStatus" persistent max-width="600px">
      <v-card lazy>
       
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-select :items="status" v-model="currentStatus" label="Status"></v-select>
              </v-flex>
              <v-flex xs12>
                   <v-menu
                    ref="menu"
                    :close-on-content-click="false"
                    v-model="menu"
                    :nudge-right="40"
                    :return-value.sync="date"
                    lazy
                    transition="scale-transition"
                    offset-y
                    full-width
                    min-width="290px"
                    >
                      <v-text-field
                        slot="activator"
                        v-model="date"
                        label="Deadline"
                        readonly
                      ></v-text-field>
                      <v-date-picker v-model="date" no-title scrollable>
                        <v-spacer></v-spacer>
                        <v-btn flat color="primary" @click="menu = false">Cancel</v-btn>
                        <v-btn flat color="primary" @click="$refs.menu.save(date)">OK</v-btn>
                      </v-date-picker>
                  </v-menu>
              </v-flex>
              <v-flex xs12>
                <v-textarea
                  label="Note"
                ></v-textarea>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="showUpdateStatus = false">Close</v-btn>
          <v-btn color="blue darken-1" flat @click="showUpdateStatus = false">Update</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>

</div>
</template>

<script src="./ManageReservations.js"></script>

<style src="./ManageReservations.scss" lang="scss"></style>
