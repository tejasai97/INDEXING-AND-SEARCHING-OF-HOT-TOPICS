<template>
  <div id="app">
    <v-layout row wrap>
      <v-flex xs12>
        <v-layout row wrap>
          <v-flex xs3>
            <!-- <v-time-picker v-model="picker" :landscape="landscape"></v-time-picker> -->

            <v-menu
              ref="menu"
              v-model="menu1"
              :close-on-content-click="false"
              :nudge-right="40"
              :return-value.sync="time"
              lazy
              transition="scale-transition"
              offset-y
              full-width
              max-width="290px"
              min-width="290px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="time"
                  label="From"
                  prepend-icon="access_time"
                  readonly
                  v-on="on"
                ></v-text-field>
              </template>
              <v-time-picker
                v-if="menu1"
                v-model="time"
                full-width
                @click:minute="$refs.menu.save(time)"
              ></v-time-picker>
            </v-menu>
            <v-spacer></v-spacer>
            <v-menu
              ref="menu_2"
              v-model="menu2"
              :close-on-content-click="false"
              :nudge-right="40"
              :return-value.sync="time2"
              lazy
              transition="scale-transition"
              offset-y
              full-width
              max-width="290px"
              min-width="290px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="time2"
                  label="To"
                  prepend-icon="access_time"
                  readonly
                  v-on="on"
                ></v-text-field>
              </template>
              <v-time-picker
                v-if="menu2"
                v-model="time2"
                full-width
                @click:minute="$refs.menu_2.save(time2)"
              ></v-time-picker>
            </v-menu>
          </v-flex>
          <v-flex xs1></v-flex>
          <v-flex xs1></v-flex>
          <div class="text-xs-center">
            <v-dialog v-model="dialog" width="500">
              <template v-slot:activator="{ on }">
                <v-btn color="info" dark v-on="on" @click="submitData">Query</v-btn>
                <v-alert :value="alert" type="error" transition="scale-transition">Couldn't fetch data</v-alert>
              </template>

              <v-card>
                <v-card-title class="headline grey lighten-2" primary-title>Sentiment</v-card-title>

                <v-card-text>The sentiment seems to be {{sentiment}}</v-card-text>

                <v-divider></v-divider>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" flat @click="dialog = false">Close</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </div>
        </v-layout>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
module.exports = {
  data: function() {
    return {
      landscape: false,
      time: null,
      time2: null,
      menu1: null,
      menu2: false,
      modal2: false,
      sentiment: null,
      dialog:false,
      alert:false,
    };
  },
  methods: {
    submitData: function() {
      axios
        .post(
          "http://localhost:5000/sentiment",
          {
            from: this.time,
            to: this.time2
          },
          { headers: { Accept: "application/json" } }
        )
        .then(response => {
          this.alert=false;
          this.sentiment = response.data;
        })
        .catch(error => {
          this.dialog=false;
          this.alert = true;
        });
    }
  }
};
</script>

