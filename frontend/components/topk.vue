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
            <v-slider
              v-model="value"
              :min="1"
              :rules="rules"
              label="K Value"
              step="1"
              thumb-label="always"
              ticks
            ></v-slider>
            <v-btn color="info" @click="submitData">Query</v-btn>
            <v-alert
              :value="alert"
              type="error"
              transition="scale-transition"
            >Couldn't fetch data</v-alert>
          </v-flex>
          <v-flex xs1></v-flex>
          <v-flex xs4>
            <v-data-table :headers="headers" :items="hitterdata">
              <template v-slot:items="props">
                <td>{{ props.item.word }}</td>
                <td>{{ props.item.count }}</td>
              </template>
            </v-data-table>
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
module.exports = {
  data() {
    return {
      headers: [
        { text: "word", value: "word" },
        { text: "count", value: "count" }
      ],
      landscape: false,
      value: 10,
      rules: [v => v <= 40 || "May increase loading time"],
      selected: null,
      time: null,
      time2: null,
      menu1: null,
      menu2: false,
      modal2: false,
      hitterdata: [],
      alert: false
    };
  },
  created: function() {
    this.submitData();
  },
  methods: {
    submitData: function() {
      axios
        .post(
          "http://localhost:5000/topK",
          {
            from: this.time,
            to: this.time2,
            k: this.value
          },
          {
            headers: {
              "Access-Control-Allow-Origin": "*",
              Accept: "application/json"
            }
          }
        )
        .then(response => {
          this.alert=false;
          this.hitterdata = response.data;
        })
        .catch(error => {
          this.alert=true;
        });
    }
  }
};
</script>

