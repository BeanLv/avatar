Vue.use(swipe);
Vue.use(hiddenpage);
new Vue({
    el: '#app',
    data: {
        operators: [],
        createpage: {
            name: '',
        },
        editpage: {
            operator: null,
            newname: ''
        },
        launched: false
    },
    methods: {
        entereditmode: function (o) {
            this.editpage.operator = o;
            this.editpage.newname = '';
            this.$refs['editpage'].show();
            window.$eventbus.$emit('swipeclear', true);
        },
        exiteditmode: function () {
            this.editpage.operator = null;
            this.editpage.newname = '';
            this.$refs['editpage'].close();
        },
        entercreatemode: function () {
            this.createpage.name = '';
            this.$refs['createpage'].show();
            window.$eventbus.$emit('swipeclear', true);
        },
        exitcreatemode: function () {
            this.createpage.name = '';
            this.$refs['createpage'].close();
        },
        updateoperator: function () {
            this.$refs['editpage'].close();
            const operatorid = this.editpage.operator.id;
            this.$patch(`/rests/operators/${operatorid}`, {name: this.editpage.newname}).then(() => {
                this.editpage.operator.name = this.editpage.newname;
                this.$toast.show();
            });
        },
        createoperator: function () {
            this.$refs['createpage'].close();
            this.$post(`/rests/operators`, {name: this.createpage.name}).then(res => {
                this.operators.push(res.data);
                this.$toast.show();
            });
        },
        deleteoperator: function (o, i) {
            this.$confirm.show('提示', '确定删除么?')
                .then(this.$delete(`/rests/operators/${o['id']}`))
                .then(() => {
                    this.operators.splice(i, 1);
                    this.$toast.show();
                });
        }
    },
    filters: {
        operatorname: function (operator) {
            return operator ? operator.name : '';
        },
        bizlisturl: function (operatorid) {
            return `/pages/bizlist?operatorid=${operatorid}`;
        },
        operatornamecss: function (name) {
            return (!name || !/^\S{1,10}$/.test(name)) ? 'weui-icon-warn' : '';
        }
    },
    computed: {
        disableupdateoperator: function () {
            return !this.editpage.operator || !this.editpage.newname ||
                this.editpage.newname === this.editpage.operator.name ||
                !/^\S{1,10}$/.test(this.editpage.newname);
        },
        disablecreateoperator: function () {
            return !this.createpage.name || !/^\S{1,10}$/.test(this.createpage.name);
        }
    },
    created: function () {
        this.$get('/rests/operators').then(res => {
            this.operators = res.data;
            this.launched = true;
        });
    }
});