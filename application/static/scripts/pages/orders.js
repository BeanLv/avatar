Vue.use(actionsheet);
new Vue({
    mixins: [mixins.order],
    el: '#app',
    data: {
        query: {owner: 0, status: 0},
        filter: {owner: 0, status: 0},
        orders: [],
        total: undefined,
        pagenum: 1,
        pagesize: 20,
        pagecount: undefined,
        searchmodeon: false
    },
    methods: {
        nextpage: function () {
            let params = {pagenum: this.pagenum + 1, pagesize: this.pagesize};
            this.query.owner && (params.owner = this.query.owner);
            this.query.status && (params.status = this.query.status);
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
        searchmode: function () {
            this.copyfilterfromquery();
            this.searchmodeon = true;
        },
        normalmode: function () {
            this.searchmodeon = false;
        },
        search: function () {
            this.searchmodeon = false;
            let params = {pagenum: 1, pagesize: this.pagesize};
            this.filter.status && (params.status = this.filter.status);
            this.filter.owner && (params.owner = this.filter.owner);
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
            this.filter.owner = this.query.owner;
        },
        copyfiltertoquery: function () {
            this.query.status = this.filter.status;
            this.query.owner = this.filter.owner;
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
        });
    }
});