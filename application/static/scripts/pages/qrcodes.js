Vue.use(swipe);
new Vue({
    el: '#app',
    data: {
        qrcodes: [],
        launched: false
    },
    methods: {
        deleteqrcode: function (qrcode, i) {
            this.$confirm.show('提示', '确定要删除么?')
                .then(() => this.$delete(`/rests/qrcodes/${qrcode.id}`))
                .then(() => {
                    this.qrcodes.splice(i, 1);
                    this.$toast.show();
                });
        }
    },
    filters: {
        qrcodepreviewurl: function (qrcode) {
            return `/qrcodes/${qrcode.id}`
        }
    },
    computed: {
        createqrcodeurl: function () {
            return `/pages/createqrcode`;
        }
    },
    created: function () {
        this.$get('/rests/qrcodes').then(res => {
            this.qrcodes = res.data;
            this.launched = true;
        });
    }
});
