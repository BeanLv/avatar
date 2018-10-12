Vue.use(actionsheet);
Vue.use(addressbook);
new Vue({
    mixins: [mixins.order],
    el: '#app',
    data: {
        query: {owner: null, status: 0},
        filter: {owner: null, status: 0},
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
            this.query.owner && (params.owner = this.query.owner.id);
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
        chooseuser: function () {
            this.$refs['addressbook'].show().then(owner => this.filter.owner = owner);
        },
        searchmode: function () {
            this.copyfilterfromquery();
            this.searchmodeon = true;
            $(document.body).css('height', `${window.innerHeight}px`);
            $(document.body).addClass('oh');
        },
        normalmode: function () {
            this.searchmodeon = false;
            $(document.body).prop('style').removeProperty('height');
            $(document.body).removeClass('oh');
        },
        search: function () {
            this.searchmodeon = false;
            let params = {pagenum: 1, pagesize: this.pagesize};
            this.filter.status && (params.status = this.filter.status);
            this.filter.owner && (params.owner = this.filter.owner.id);
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
    filters: {
        ownername: function (owner) {
            return owner ? owner.name : '所有人';
        },
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