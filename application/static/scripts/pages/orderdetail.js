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
        operatorname: '',
        status: 0,
        installtime: 0,
        ismanager: false,
        issource: false,
        ishandler: false,
        sourcename: '',
        handlername: '',
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
                    const operation = {operation: 2, handler: user.id};
                    return this.operateorder(operation);
                }).then(res => {
                    this.handler = user.id;
                    this.handlername = user.name;
                    this.ishandler = res.data['ishandler'] || false;
                    this.status = 2;
                });
            });
        },
        dealwithorder: function () {
            this.$confirm.show('提示', '确定接单么？')
                .then(() => this.operateorder({operation: 3}))
                .then(res => {
                    this.ishandler = true;
                    this.handlername = res.data;
                    this.status = 2;
                });
        },
        finishorder: function () {
            this.$confirm.show('提示', '确定完成么？').then(() => this.operateorder({operation: 4}))
                .then(() => this.status = 3);
        },
        closeorder: function () {
            this.$confirm.show('提示', '确定关闭么？').then(() => this.operateorder({operation: 6}))
                .then(() => this.status = 5);
        },
        operateorder: function (operation) {
            return new Promise(resolve => {
                this.$post(`/rests/orders/${this.id}/operations`, operation).then(res => {
                    if (res.status === 412) {
                        this.$prompt.show('异常', '订单状态异常，请刷新页面', true);
                    } else {
                        res.data['handler'] && (this.handler = res.data['handler']);
                        this.status = res.data['status'];
                        this.$prompt.show('成功', '操作成功');
                        resolve(res);
                    }
                });
            });
        }
    },
    filters: {
        name: function (name) {
            return name || '无'
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
            return this.status === 1 && (this.ismanager || this.issource);
        },
        canfinish: function () {
            return this.status === 2 && (this.ismanager || this.ishandler);
        },
        canclose: function () {
            return this.ismanager || this.issource || (this.status === 2 && this.ishandler);
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
            this.operatorname = order.operatorname;
            this.status = order.status;
            this.installtime = order.installtime;
            this.ismanager = order.ismanager;
            this.issource = order.source;
            this.ishandler = order.ishandler;
            this.sourcename = order.sourcename;
            this.handlername = order.handlername;
            this.launched = true;
        });
    }
});