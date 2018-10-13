Vue.use(qrcodeselect);
Vue.use(hiddenpage);
new Vue({
    el: '#app',
    data: {
        today: 0,
        thisweek: 0,
        thismonth: 0,
        thisseason: 0,
        halfyear: 0,
        thisyear: 0,
        launched: false,
        query: {source: null},
        filter: {source: null}
    },
    methods: {
        getstatistic: function (query) {
            return new Promise(resolve => {
                let params = {};
                query.source && (params.source = query.source.id);
                this.$get('/rests/statistics/pageview', {params: params}).then(res => {
                    this.today = res.data['today'];
                    this.thisweek = res.data['thisweek'];
                    this.thismonth = res.data['thismonth'];
                    this.thisseason = res.data['thisseason'];
                    this.halfyear = res.data['halfyear'];
                    this.thisyear = res.data['thisyear'];
                    resolve()
                });
            });
        },
        enterfiltmode: function () {
            this.filter.source = this.query.source;
            this.$refs['hiddenpage'].show();
        },
        exitfiltmode: function () {
            this.$refs['hiddenpage'].close();
        },
        filt: function () {
            this.$refs['hiddenpage'].close();
            this.getstatistic(this.filter).then(() => {
                this.query.source = this.filter.source;
            });
        },
        choosesource: function () {
            this.$refs['qrcodeselect'].show().then(source => {
                this.filter.source = source;
            });
        }
    },
    filters: {
        sourcename: function (source) {
            return source ? source.name : '所有';
        }
    },
    created: function () {
        this.getstatistic(this.query).then(() => this.launched = true);
    }
});