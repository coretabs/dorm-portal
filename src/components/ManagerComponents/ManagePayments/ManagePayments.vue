<template>
<div id="manage-rooms">
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
          <div  @click="filterStatus(lang.manageResrevations.confirmed)">
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

                  <v-menu v-if="props.item.receipts.length > 1" offset-y>
                    <v-btn class="receipts-btn" slot="activator" depressed flat>
                      {{lang.manageResrevations.download}} <v-icon color="#999" >expand_more</v-icon>
                    </v-btn>
                    <v-list>
                      <v-list-tile v-for="(receipt,i) in props.item.receipts" :key="i" >
                        <a :href="receipt" download>{{lang.manageResrevations.receipt}} {{i+1}}</a>
                      </v-list-tile>
                    </v-list>
                  </v-menu>
                  <a v-else v-for="(receipt,i) in props.item.receipts" :key="i"  :href="receipt" download>{{lang.manageResrevations.receipt}}</a>

                </td>
                <td class="text-xs-left">{{ props.item.status }}</td>
                <td class="text-xs-left">{{ props.item.name }}</td>
                <td class="text-xs-left">{{ props.item.email }}</td>
                <td class="text-xs-left">{{ props.item.submittedOn }}</td>
                <td class="text-xs-left">{{ props.item.deadline }}</td>
                <td class="justify-center layout px-0">
                  <v-btn v-if="props.item.status.toLowerCase() != lang.manageResrevations.confirmed.toLowerCase()" color="green" dark depressed>{{lang.manageResrevations.updateStatus}}</v-btn>
                  <v-btn v-else color="#feae25" depressed>{{lang.manageResrevations.askForReview}}</v-btn>
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
</div>
</template>

<script src="./ManagePayments.js"></script>

<style src="./ManagePayments.scss" lang="scss"></style>
