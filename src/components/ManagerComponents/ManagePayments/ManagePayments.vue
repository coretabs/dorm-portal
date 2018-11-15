<template>
<div id="manage-rooms">
  <v-card>
    <v-card-text>
      <v-layout id="statistics-cards" wrap>

        <v-flex xs12 md3>
          <div>
            <h3>Wating</h3>
            <span>25</span>
          </div>
        </v-flex>

        <v-flex xs6 md3>
          <div>
            <h3>Pending</h3>
            <span>12</span>
          </div>
        </v-flex>

        <v-flex xs6 md2>
          <div>
            <h3>Confirmed</h3>
            <span>125</span>
          </div>
        </v-flex>

        <v-flex xs6 md2>
          <div>
            <h3>Rejected</h3>
            <span>35</span>
          </div>
        </v-flex>

        <v-flex xs6 md2>
          <div>
            <h3>Unpaid</h3>
            <span>28</span>
          </div>
        </v-flex>

      </v-layout>

      <v-layout id="" wrap>
        <v-flex xs12>
            <v-card class="elevation-0">
              <v-card-title>
                <strong>Payments Records</strong>
                <v-spacer></v-spacer>
                <v-text-field
                  v-model="search"
                  append-icon="search"
                  label="Search"
                  single-line
                  hide-details
                ></v-text-field>
              </v-card-title>
              <v-data-table
                :headers="headers"
                :items="payments"
                :search="search"
              >
                <template slot="items" slot-scope="props">
                  <td class="text-xs-left">{{ props.item.amount }}</td>
                  <td class="text-xs-left">{{ props.item.name }}</td>
                  <td class="text-xs-left">{{ props.item.email }}</td>
                  <td class="text-xs-left">{{ props.item.submittedOn }}</td>
                  <td class="text-xs-left">{{ props.item.deadline }}</td>
                  <td class="text-xs-left">{{ props.item.status }}</td>
                  <td class="text-xs-left">
                    <a v-for="(receipt,i) in props.item.receipts" :key="i" :href="receipt" download>
                      receipt
                    </a>
                  </td>
                  <td class="justify-center layout px-0">
                    <v-btn color="green" dark depressed>Update Status</v-btn>
                  </td>
                </template>
                <v-alert slot="no-results" :value="true" color="error" icon="warning">
                  Your search for "{{ search }}" found no results.
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
