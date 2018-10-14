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
        previewqrcodeurl: function (qrcode) {
            return `/public/pages/qrcodes/${qrcode.id}`
        }
    },
    computed: {
        createqrcodeurl: function () {
            return `/pages/qrcodecreate`;
        }
    },
    created: function () {
        this.$get('/rests/qrcodes').then(res => {
            this.qrcodes = res.data;
            this.launched = true;
        });
    }
});
