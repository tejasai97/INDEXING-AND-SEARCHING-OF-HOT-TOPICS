<template>
  <div id="app">
    <v-layout row wrap>
      <v-flex xs12>
        <v-layout row wrap>
          <v-flex xs3>
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
          <v-flex xs3>
            <v-text-field label="Term" placeholder="Enter Here" v-model="term" outline></v-text-field>
            <v-slider
              v-model="no_tweets"
              :rules="rules"
              label="Number of Tweets"
              step="1"
              thumb-label="always"
              ticks
            ></v-slider>
            <v-btn color="info" @click="submitData">Query</v-btn>
            <v-alert :value="alert" type="error" transition="scale-transition">Couldn't fetch data</v-alert>
          </v-flex>
          <v-flex xs1></v-flex>
          <v-flex xs3>
            <v-card color="white" dark flat tile>
              <v-window v-model="onboarding">
                <v-window-item v-for="n in length" :key="`card-${n}`">
                  <v-card class="mx-auto" color="#26c6da" dark max-width="800">
                    <v-card-title>
                      <i class="fa fa-twitter" style="font-size:28px;color:white"></i>
                      <span class="title font-weight-light">Twitter</span>
                    </v-card-title>

                    <v-card-text class="headline font-weight-bold">{{tweets[n]}}</v-card-text>
                  </v-card>
                </v-window-item>
              </v-window>

              <v-card-actions>
                <v-btn color="info" @click="prev">Previous</v-btn>
                <v-btn color="info" @click="next">Next</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
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
      term: null,
      rules: [v => v <= 40 || "May increase loading time"],
      selected: null,
      time: null,
      time2: null,
      menu1: null,
      menu2: false,
      modal2: false,
      tweets: [],
      length: 0,
      onboarding: 0,
      no_tweets: 5,
      alert: false,
      rules: [v => v <= 40 || "May increase loading time"]
    };
  },
  methods: {
    submitData: function() {
      this.tweets = [];
      axios
        .post(
          "http://localhost:5000/term",
          {
            from: this.time,
            to: this.time2,
            term: this.term,
            k: this.no_tweets
          },
          { headers: { Accept: "application/json" } }
        )
        .then(response => {
          this.alert = false;
          this.tweets = response.data;
          this.length = response.data.length - 1;
          if (this.length < 0) {
            this.length = 0;
          }
        })
        .catch(error => {
          this.alert = true;
        });
    },
    next() {
      this.onboarding =
        this.onboarding + 1 === this.length ? 0 : this.onboarding + 1;
    },
    prev() {
      this.onboarding =
        this.onboarding - 1 < 0 ? this.length - 1 : this.onboarding - 1;
    }
  }
};
</script>

