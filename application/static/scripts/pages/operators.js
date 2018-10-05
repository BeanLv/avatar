new Vue({
    el: '#app',
    data: {
        operators: [],
        createform: {
            show: false,
            name: ''
        },
        launched: false
    },
    methods: {
        startCreate: function () {
            this.createform.show = true;
            this.createform.name = '';
            this.$swipitem && this.$swipitem.blur();
            this.$swipitem = null;
        },
        cancelCreate: function () {
            this.createform.show = false;
            this.createform.name = '';
        },
        confirmCreate: function () {
            this.$post('/rests/operators', {name: this.createform.name}).then(res => {
                this.operators.push(res.data);
                this.createform.name = '';
                this.$prompt.show('成功', '添加成功');
            });
        },
        swipestart: function (item) {
            this.$swipitem && this.$swipitem !== item && this.$swipitem.blur();
            this.$swipitem = item;
            this.cancelCreate();
        },
        swipeupdate: function (operator) {
            this.$patch(`/rests/operators/${operator.id}`, {name: operator.name}).then(() => {
                this.operators[operator['index']].name = operator.name;
                this.$swipitem && this.$swipitem.blur();
                this.$prompt.show('成功', '修改成功');
            });
        },
        swipedelete: function (operator) {
            this.$delete(`/rests/operators/${operator.id}`).then(() => {
                this.operators.splice(operator.index, 1);
                this.$prompt.show('成功', '删除成功');
            });
        },
    },
    filters: {
        operatorbizsurl: function (operatorid) {
            return `/pages/operatorbizs?operatorid=${operatorid}`;
        }
    },
    computed: {
        disablecreate: function () {
            return !/^\S{1,10}$/.test(this.createform.name);
        }
    },
    created: function () {
        this.$get('/rests/operators').then(res => {
            this.operators = res.data;
            this.launched = true;
        });
    }
});