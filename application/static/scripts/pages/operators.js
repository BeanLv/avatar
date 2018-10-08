Vue.use(swipe);
new Vue({
    el: '#app',
    data: {
        operators: [],
        createform: {
            show: false,
            name: ''
        },
        editingoperator: null,
        launched: false
    },
    methods: {
        editoperator: function (o) {
            this.editingoperator = o;
            o.editing = true;
            o.newname = '';
        },
        canceleditoperator: function (o) {
            this.editingoperator = null;
            o.editing = false;
            o.newname = '';
            window.$eventbus.$emit('swipeclear');
        },
        updateoperator: function (o) {
            this.$patch(`/rests/operators/${o['id']}`, {name: o.newname}).then(() => {
                o.name = o.newname;
                this.canceleditoperator(o);
                this.$prompt.show('成功', '编辑成功');
                window.$eventbus.$emit('swipeclear');
            });
        },
        deleteoperator: function (o, i) {
            this.$confirm.show('提示', '确定删除么?')
                .then(this.$delete(`/rests/operators/${o['id']}`))
                .then(() => {
                    this.operators.splice(i, 1);
                    this.$toast.show();
                });
        },
        opencreateform: function () {
            this.createform.show = true;
            this.createform.name = '';
            this.editingoperator && this.canceleditoperator(this.editingoperator);
            window.$eventbus.$emit('swipeclear', true);
        },
        closecreateform: function () {
            this.createform.show = false;
            this.createform.name = '';
        },
        createoperator: function () {
            this.$post('/rests/operators', {name: this.createform.name}).then(res => {
                res.data.editing = false;
                res.data.newname = '';
                this.operators.push(res.data);
                this.createform.name = '';
                this.$prompt.show('成功', '添加成功');
            });
        },
        onswipestart: function () {
            this.editingoperator && this.canceleditoperator(this.editingoperator);
            this.createform.show && this.closecreateform();
        }
    },
    filters: {
        operatorbizsurl: function (operatorid) {
            return `/pages/operatorbizs?operatorid=${operatorid}`;
        },
        disableupdateoperator: function (o) {
            return !o.newname || (o.name === o.newname) || !/^\S{1,10}$/.test(o.newname);
        }
    },
    computed: {
        disablecreateoperator: function () {
            return !this.createform.name || !/^\S{1,10}$/.test(this.createform.name);
        }
    },
    created: function () {
        this.$get('/rests/operators').then(res => {
            res.data.forEach(o => {
                o.editing = false;
                o.newname = '';
            });
            this.operators = res.data;
            this.launched = true;
        });
    },
    mounted: function () {
        window.$eventbus.$on('swipestart', this.onswipestart);
    },
    beforeDestroy: function () {
        window.$eventbus.$off('swipestart', this.onswipestart);
    }
});