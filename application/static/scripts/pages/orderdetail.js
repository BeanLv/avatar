Vue.use(actionsheet);
Vue.use(addressbook);
Vue.use(hiddenpage);
new Vue({
    el: '#app',
    mixins: [mixins.strtime, mixins.order],
    data: {
        id: 0,
        realname: '',
        nickname: '',
        headimgurl: '',
        mobile: '',
        address: '',
        bizname: '',
        opname: '',
        status: 0,
        source: '',
        installtime: 0,
        ismanager: false,
        isowner: false,
        ishandler: false,
        handler: '',
        launched: false
    },
    methods: {
        operate: function (operation) {
            this.$confirm.show().then(o => this.$post(`/rests/orders/${this.id}/operations`, {operation: operation}))
                .then(res => {
                    if (res.status === 201) {
                        this.status = res.data['status'];
                        this.records.push(res.data['record']);
                        this.$prompt.show('成功', '操作成功');
                    }
                    else {
                        this.$prompt.show('错误', '订单状态异常，请刷新页面', true);
                    }
                });
        },
        chooseaction: function (name, action) {
            const operation = action.actionvalue;
            let handlers = {
                dispatch: this.dispatchorder,
                dealwith: this.dealwithorder,
                finish: this.finishorder,
                close: this.closeorder
            };
            handlers[operation]();
        },
        dispatchorder: function () {
            this.$refs['addressbook'].show().then(user => {
                this.$confirm.show('提示', `你选择了 ${user.name}`).then(() => {
                    const operation = {operation: 2, user: user.id};
                    this.operateorder(operation);
                });
            });
        },
        dealwithorder: function () {
            this.$confirm.show('提示', '确定接单么？').then(() => this.operateorder({operation: 3}));
        },
        finishorder: function () {
            this.$confirm.show('提示', '确定完成么？').then(() => this.operateorder({operation: 4}));
        },
        closeorder: function () {
            this.$confirm.show('提示', '确定关闭么？').then(() => this.operateorder({operation: 6}));
        },
        operateorder: function (operation) {
            this.$post(`/rests/orders/${this.id}/operations`, operation).then(res => {
                if (res.status === 412) {
                    this.$prompt('异常', '订单状态异常，请刷新页面', true);
                } else {
                    res.data['handler'] && (this.handler = res.data['handler']);
                    this.status = res.data['status'];
                    this.$prompt('成功', '操作成功');
                }
            });
        }
    },
    filters: {
        username: function (username) {
            return username || '无'
        },
        mobilehref: function (mobile) {
            return 'tel:' + mobile;
        }
    },
    computed: {
        candispatch: function () {
            return this.status === 1 && this.ismanager;
        },
        candealwith: function () {
            return this.status === 1 && (this.ismanager || this.isowner);
        },
        canfinish: function () {
            return this.status === 2 && (this.ismanager || this.ishandler);
        },
        canclose: function () {
            return this.ismanager || this.isowner || (this.status === 2 && this.ishandler);
        },
        hasoperations: function () {
            return this.status === 1 || this.status === 2;
        }
    },
    created: function () {
        let id = Number(new URL(window.location.href).searchParams.get('orderid'));
        if (!id) return;
        this.$get(`/rests/orders/${id}`).then(res => {
            const order = res.data;
            this.id = order.id;
            this.realname = order.realname;
            this.nickname = order.nickname;
            this.headimgurl = order.headimgurl;
            this.mobile = order.mobile;
            this.address = order.address;
            this.bizname = order.bizname;
            this.opname = order.opname;
            this.status = order.status;
            this.source = order.source;
            this.installtime = order.installtime;
            this.ismanager = order.ismanager;
            this.isowner = order.isowner;
            this.ishandler = order.ishandler;
            this.launched = true;
        });
    }
});