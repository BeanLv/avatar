Vue.use(addressbook);
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
        waiting: 0,
        working: 0,
        done: 0,
        filter: {source: null, handler: null},
        query: {surce: null, handler: null},
        launched: false
    },
    methods: {
        getstatistic: function (query) {
            return new Promise(resolve => {
                let params = {};
                query.source && (params.source = query.source.id);
                query.handler && (params.handler = query.handler.id);
                this.$get('/rests/statistics/order', {params: params}).then(res => {
                    this.today = res.data['today'];
                    this.thisweek = res.data['thisweek'];
                    this.thismonth = res.data['thismonth'];
                    this.thisseason = res.data['thisseason'];
                    this.halfyear = res.data['halfyear'];
                    this.thisyear = res.data['thisyear'];
                    this.waiting = res.data['waiting'];
                    this.working = res.data['working'];
                    this.done = res.data['done'];
                    resolve();
                });
            });
        },
        enterfiltmode: function () {
            this.filter.surce = this.query.source;
            this.filter.handler = this.query.handler;
            this.$refs['hiddenpage'].show();
        },
        exitfiltmode: function () {
            this.$refs['hiddenpage'].close();
        },
        choosehandler: function () {
            this.$refs['addressbook'].show().then(handler => this.filter.handler = handler);
        },
        choosesource: function () {
            this.$refs['qrcodeselect'].show().then(qrcode => this.filter.source = qrcode);
        },
        filt: function () {
            this.$refs['hiddenpage'].close();
            this.getstatistic(this.filter).then(() => {
                this.query.handler = this.filter.handler;
                this.query.source = this.filter.source;
            });
        }
    },
    filters: {
        handlername: function (handler) {
            return handler ? handler.name : '所有人';
        },
        sourcename: function (source) {
            return source ? source.name : '所有';
        }
    },
    created: function () {
        this.getstatistic(this.query).then(() => this.launched = true);
    }
});