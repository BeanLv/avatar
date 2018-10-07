new Vue({
    el: '#app',
    mixins: [mixins.strtime, mixins.order],
    data: {
        id: 0,
        status: 0,
        realname: '',
        mobile: '',
        address: '',
        bizname: '',
        installtime: 0,
        openid: '',
        nickname: '',
        headimgurl: '',
        records: [],
        showrecords: false,
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
        }
    },
    created: function () {
        let id = Number(new URL(window.location.href).searchParams.get('orderid'));
        if (!id) return;
        this.$get(`/rests/orders/${id}`).then(res => {
            const order = res.data;
            this.id = order.id;
            this.status = order.status;
            this.realname = order.realname;
            this.mobile = order.mobile;
            this.address = order.address;
            this.bizname = order.bizname;
            this.installtime = order.installtime;
            this.openid = order.openid;
            this.nickname = order.nickname;
            this.headimgurl = order.headimgurl;
            this.records = order.records;
            this.launched = true;
        });
    }
});