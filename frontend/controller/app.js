Vue.use(httpVueLoader);

var app = new Vue({
  el: '#app',
  components: {
    "sentiment": "url:components/Sentiment.vue",
    "home": "url:components/topk.vue",
    "term": "url:components/term.vue",
    "prefix": "url:components/prefix.vue",
    "termset": "url:components/termset.vue"
  },
  data: {
    drawer: false,
    sentiment: false,
    home: true,
    term:false,
    prefix:false,
    termset:false,
  },
  methods: {
    display: function (data) {
      this.home = false;
      this.sentiment = false;
      this.term = false;
      this.prefix =false;
      this.termset=false;
      if (data == "home") {
        this.home = true;
      }
      if (data == "sentiment") {
        this.sentiment = true;
      }
      if(data =="term"){
        this.term=true;
      }
      if(data =="prefix"){
        this.prefix=true;
      }
      if(data=="termset"){
        this.termset=true;
      }
    }
  }
})