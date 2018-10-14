Vue.use(actionsheet);
Vue.use(addressbook);
Vue.use(qrcodeselect);
Vue.use(hiddenpage);
new Vue({
    mixins: [mixins.order],
    el: '#app',
    data: {
        query: {handler: null, source: null, status: 0},
        filter: {handler: null, source: null, status: 0},
        orders: [],
        total: undefined,
        pagenum: 1,
        pagesize: 20,
        pagecount: undefined,
        launched: false
    },
    methods: {
        nextpage: function () {
            let params = this.getqueryparams(this.pagenum + 1, this.pagesize, this.query);
            this.$get('/rests/orders', {params: params}).then(res => {
                const data = res.data;
                this.orders = this.orders.concat(data.orders);
                this.pagenum = data.pagenum;
                this.pagesize = data.pagesize;
                this.pagecount = data.pagecount;
                this.total = data.total;
            });
        },
        chooseaction: function (name, action) {
            this.filter[name] = action.actionvalue;
        },
        chooseuser: function () {
            this.$refs['addressbook'].show().then(handler => this.filter.handler = handler);
        },
        choosesource: function () {
            this.$refs['qrcodeselect'].show().then(source => this.filter.source = source);
        },
        entersearchmode: function () {
            this.copyfilterfromquery();
            this.$refs['hiddenpage'].show();
        },
        exitsearchmode: function () {
            this.$refs['hiddenpage'].close();
        },
        search: function () {
            this.$refs['hiddenpage'].close();
            let params = this.getqueryparams(1, this.pagesize, this.filter);
            this.$get('/rests/orders', {params: params}).then(res => {
                const data = res.data;
                this.orders = data.orders;
                this.pagenum = data.pagenum;
                this.pagesize = data.pagesize;
                this.pagecount = data.pagecount;
                this.total = data.total;
                this.copyfiltertoquery();
            });
        },
        copyfilterfromquery: function () {
            this.filter.status = this.query.status;
            this.filter.handler = this.query.handler;
        },
        copyfiltertoquery: function () {
            this.query.status = this.filter.status;
            this.query.handler = this.filter.handler;
        },
        getqueryparams: function (pagenum, pagesize, extra) {
            let params = {pagenum: pagenum, pagesize: pagesize};
            extra.handler && (params.handler = extra.handler.id);
            extra.source && (params.source = extra.source.id);
            extra.status && (params.status = extra.status);
            return params;
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
    mounted: function () {
        this.$get('/rests/orders').then(res => {
            const data = res.data;
            this.orders = data.orders;
            this.pagenum = data.pagenum;
            this.pagesize = data.pagesize;
            this.pagecount = data.pagecount;
            this.total = data.total;
            this.launched = true;
        });
    }
});